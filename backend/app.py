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

import pickle
import traceback

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = "XGmodel.pkl"

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
# Categorical -> numeric encoding
# NOTE: We don't have the original LabelEncoder used during training.
# This uses sklearn's LabelEncoder DEFAULT behaviour (alphabetical sort),
# which is the most common convention. If predictions look off, ask your
# leader for the actual encoder/mapping and swap these dicts.
# ---------------------------------------------------------------------------
FESTIVAL_NAME_OPTIONS = [
    "None", "Diwali", "Holi", "Raksha Bandhan", "Navratri",
    "Eid", "Christmas", "Republic Day", "Independence Day", "Dussehra",
]
FESTIVAL_TYPE_OPTIONS = ["None", "National", "Regional", "Religious"]
REGION_OPTIONS = [
    "Prayagraj Urban", "Prayagraj Rural", "Lucknow Central", "Varanasi Cluster",
]

def _encode_map(options):
    return {name: i for i, name in enumerate(sorted(options))}

FESTIVAL_NAME_MAP = _encode_map(FESTIVAL_NAME_OPTIONS)
FESTIVAL_TYPE_MAP = _encode_map(FESTIVAL_TYPE_OPTIONS)
REGION_MAP = _encode_map(REGION_OPTIONS)

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


def encode_payload(payload):
    """Convert incoming JSON dict (raw form values) into the numeric
    array the model expects, in the correct feature order."""
    row = []
    for feat in FEATURE_ORDER:
        val = payload.get(feat)
        if val is None:
            raise ValueError(f"Missing field: {feat}")

        if feat == "festival_name":
            row.append(FESTIVAL_NAME_MAP.get(val, FESTIVAL_NAME_MAP["None"]))
        elif feat == "festival_type":
            row.append(FESTIVAL_TYPE_MAP.get(val, FESTIVAL_TYPE_MAP["None"]))
        elif feat == "region":
            row.append(REGION_MAP.get(val, 0))
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
    return jsonify({
        "model_type": type(model).__name__,
        "n_features": len(FEATURE_ORDER),
        "feature_names": FEATURE_ORDER,
        "options": {
            "festival_name": FESTIVAL_NAME_OPTIONS,
            "festival_type": FESTIVAL_TYPE_OPTIONS,
            "region": REGION_OPTIONS,
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
        return jsonify({
            "prediction": float(prediction[0]),
            "encoded_input": dict(zip(FEATURE_ORDER, row)),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Backend is running", "model_loaded": model is not None})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
