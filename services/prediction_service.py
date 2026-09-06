"""
Prediction service
-------------------
Single source of truth for:
  * loading the existing trained model (XGmodel.pkl)
  * loading the existing label encoders (label_encoders.pkl)
  * the exact feature order the model was trained on
  * converting a raw JSON payload into the numeric row the model expects
  * running the prediction

NOTHING in this file changes the model, the encoders, the feature order,
or the encoding behavior. It is a straight, path-safe port of the logic
that used to live directly in backend/app.py.
"""

import os
import pickle
import traceback

import numpy as np

# ---------------------------------------------------------------------------
# Path safety: resolve everything relative to this file's location, never
# relative to the current working directory.
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
MODEL_PATH = os.path.join(BASE_DIR, "XGmodel.pkl")

ENCODERS_PATHS = [
    os.path.join(BASE_DIR, "..", "Model", "label_encoders.pkl"),
    os.path.join(BASE_DIR, "Model", "label_encoders.pkl"),
    os.path.join(BASE_DIR, "label_encoders.pkl"),
]

# ---------------------------------------------------------------------------
# Exact feature order the model expects (from n_features_in_ / feature_names_in_)
# DO NOT CHANGE THIS ORDER.
# ---------------------------------------------------------------------------
FEATURE_ORDER = [
    "store", "item", "year", "month", "day", "weekday",
    "festival_name", "festival_type", "region", "impact_scale",
    "is_regional_event", "days_to_next_festival",
    "is_festival_day", "pre_festival_week",
]

# ---------------------------------------------------------------------------
# Fallback options (in case label_encoders.pkl is missing)
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

# Weekday mapping from index to string name (matching frontend select indices)
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------------------------------------------------------------------------
# Load label encoders (read-only, never regenerated/retrained)
# ---------------------------------------------------------------------------
encoders = None
for _path in ENCODERS_PATHS:
    if os.path.exists(_path):
        try:
            with open(_path, "rb") as f:
                encoders = pickle.load(f)
            print(f"[OK] Label encoders loaded from {_path}")
            break
        except Exception as e:
            print(f"[WARNING] Failed to load encoders from {_path}: {e}")

# ---------------------------------------------------------------------------
# Load model once at startup (read-only, never retrained/regenerated)
# ---------------------------------------------------------------------------
model = None
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print(f"[OK] Model loaded: {type(model)}")
except Exception as e:
    print("[ERROR] Could not load model:", e)
    traceback.print_exc()


def is_model_loaded():
    return model is not None


def get_model_type_name():
    return type(model).__name__ if model is not None else None


def get_options():
    """Categorical options for populating frontend dropdowns, sourced from
    the existing label_encoders.pkl when available."""
    if encoders is not None:
        return {
            "festival_name": list(encoders["festival_name"].classes_),
            "festival_type": list(encoders["festival_type"].classes_),
            "region": list(encoders["region"].classes_),
        }
    return {
        "festival_name": FALLBACK_FESTIVAL_NAMES,
        "festival_type": FALLBACK_FESTIVAL_TYPES,
        "region": FALLBACK_REGIONS,
    }


def encode_payload(payload):
    """Convert incoming JSON dict (raw form values) into the numeric
    array the model expects, in the correct feature order.

    This is an unmodified port of the original encoding logic — same
    per-feature normalization, same label-encoder lookups, same
    fallback-for-unseen-labels behavior.
    """
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


def _to_json_safe(x):
    if hasattr(x, "item"):
        return x.item()
    if isinstance(x, (np.integer, np.int64, np.int32)):
        return int(x)
    if isinstance(x, (np.floating, np.float64, np.float32)):
        return float(x)
    return x


def run_prediction(payload):
    """Encode payload, run model.predict(), return (prediction, encoded_input)."""
    row = encode_payload(payload)
    X = np.array(row).reshape(1, -1)
    prediction = model.predict(X)
    encoded_input = dict(zip(FEATURE_ORDER, (_to_json_safe(x) for x in row)))
    return float(prediction[0]), encoded_input
