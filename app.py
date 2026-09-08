"""
Backend for the Festive-Aware Demand Forecast Model (XGBoost)
---------------------------------------------------------------
Loads XGmodel.pkl and exposes a REST API for the frontend dashboard.

SETUP (on your own machine):
    pip install -r requirements.txt

RUN:
    python app.py

Server starts at http://127.0.0.1:5000
"""

import os
import pickle
import traceback

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = "XGmodel.pkl"

# Paths to search for label encoders
ENCODERS_PATHS = [
    "../Model/label_encoders.pkl",
    "Model/label_encoders.pkl",
    "label_encoders.pkl"
]

# ---------------------------------------------------------------------------
# Exact feature order the model expects (from n_features_in_ / feature_names_in_)
# ---------------------------------------------------------------------------
FEATURE_ORDER = [
    "store", "item", "year", "month", "day", "weekday",
    "festival_name", "festival_type", "region", "impact_scale",
    "is_regional_event", "days_to_next_festival",
    "is_festival_day", "pre_festival_week",
]

# ---------------------------------------------------------------------------
# Fallback Options (in case label_encoders.pkl is missing)
# ---------------------------------------------------------------------------
FALLBACK_FESTIVAL_NAMES = [
    "None", "Diwali", "Holi", "Raksha Bandhan", "Navratri",
    "Eid", "Christmas", "Republic Day", "Independence Day", "Dussehra",
]
FALLBACK_FESTIVAL_TYPES = ["None", "National", "Regional", "Religious"]
FALLBACK_REGIONS = [
    "Prayagraj Urban", "Prayagraj Rural", "Lucknow Central", "Varanasi Cluster",
]

def _encode_map(options):
    return {name: i for i, name in enumerate(sorted(options))}

FALLBACK_FESTIVAL_NAME_MAP = _encode_map(FALLBACK_FESTIVAL_NAMES)
FALLBACK_FESTIVAL_TYPE_MAP = _encode_map(FALLBACK_FESTIVAL_TYPES)
FALLBACK_REGION_MAP = _encode_map(FALLBACK_REGIONS)

# ---------------------------------------------------------------------------
# Load label encoders
# ---------------------------------------------------------------------------
encoders = None
for path in ENCODERS_PATHS:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                encoders = pickle.load(f)
            print(f"[OK] Label encoders loaded from {path}")
            break
        except Exception as e:
            print(f"[WARNING] Failed to load encoders from {path}: {e}")

# ---------------------------------------------------------------------------
# Load model once at startup
# ---------------------------------------------------------------------------
model = None
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print(f"[OK] Model loaded: {type(model)}")
except Exception as e:
    print("[ERROR] Could not load model:", e)
    traceback.print_exc()


# Weekday mapping from index to string name (matching frontend select indices)
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def encode_payload(payload):
    """Convert incoming JSON dict (raw form values) into the numeric
    array the model expects, in the correct feature order."""
    row = []
    for feat in FEATURE_ORDER:
        val = payload.get(feat)
        if val is None:
            raise ValueError(f"Missing field: {feat}")

        if encoders is not None and feat in encoders:
            le = encoders[feat]
            # Custom input normalization per feature
            if feat == "weekday":
                # Convert frontend weekday index to weekday name
                try:
                    weekday_idx = int(float(val))
                    val_str = WEEKDAY_NAMES[weekday_idx]
                except (ValueError, IndexError):
                    val_str = "Monday"
            elif feat == "impact_scale":
                try:
                    val_num = int(float(val))
                    if val_num > 10:
                        val_num = int(val_num / 10)  # Map 50 to 5
                    val_str = str(val_num)
                except ValueError:
                    val_str = "0"
            else:
                val_str = str(val)

            # Map using the loaded label encoder with a fallback for unseen labels
            if val_str in le.classes_:
                row.append(le.transform([val_str])[0])
            else:
                fallback_val = "None" if "None" in le.classes_ else ("0" if "0" in le.classes_ else le.classes_[0])
                row.append(le.transform([fallback_val])[0])

        else:
            # Fallback legacy encoding logic
            if feat == "festival_name":
                row.append(FALLBACK_FESTIVAL_NAME_MAP.get(val, FALLBACK_FESTIVAL_NAME_MAP["None"]))
            elif feat == "festival_type":
                row.append(FALLBACK_FESTIVAL_TYPE_MAP.get(val, FALLBACK_FESTIVAL_TYPE_MAP["None"]))
            elif feat == "region":
                row.append(FALLBACK_REGION_MAP.get(val, 0))
            elif feat in ("is_regional_event", "is_festival_day", "pre_festival_week"):
                row.append(1 if val in (True, "true", "1", 1) else 0)
            else:
                row.append(float(val))
    return row


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/model-info", methods=["GET"])
def model_info():
    if model is None:
        return jsonify({"error": "Model failed to load on server."}), 500
    
    if encoders is not None:
        fest_names = list(encoders['festival_name'].classes_)
        fest_types = list(encoders['festival_type'].classes_)
        regions = list(encoders['region'].classes_)
    else:
        fest_names = FALLBACK_FESTIVAL_NAMES
        fest_types = FALLBACK_FESTIVAL_TYPES
        regions = FALLBACK_REGIONS

    return jsonify({
        "model_type": type(model).__name__,
        "n_features": len(FEATURE_ORDER),
        "feature_names": FEATURE_ORDER,
        "options": {
            "festival_name": fest_names,
            "festival_type": fest_types,
            "region": regions,
        },
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Expects JSON body with all 14 named fields, e.g.:
    {
      "store": 1, "item": 5, "year": 2026, "month": 8, "day": 28,
      "weekday": 4, "festival_name": "Raksha Bandhan",
      "festival_type": "Religious", "region": "Lucknow Central",
      "impact_scale": 70, "is_regional_event": false,
      "days_to_next_festival": 2, "is_festival_day": false,
      "pre_festival_week": true
    }
    """
    if model is None:
        return jsonify({"error": "Model not loaded on server."}), 500

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Send a JSON body with all 14 fields."}), 400

    try:
        row = encode_payload(data)
        X = np.array(row).reshape(1, -1)
        prediction = model.predict(X)
        
        # Convert row elements to standard Python types for JSON serializability
        serializable_row = []
        for x in row:
            if hasattr(x, "item"):
                serializable_row.append(x.item())
            elif isinstance(x, (np.integer, np.int64, np.int32)):
                serializable_row.append(int(x))
            elif isinstance(x, (np.floating, np.float64, np.float32)):
                serializable_row.append(float(x))
            else:
                serializable_row.append(x)

        return jsonify({
            "prediction": float(prediction[0]),
            "encoded_input": dict(zip(FEATURE_ORDER, serializable_row)),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Backend is running", "model_loaded": model is not None})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
