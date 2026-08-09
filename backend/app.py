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
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "Model", "ML model", "XGmodel.pkl")

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
# Exact mappings matching training LabelEncoders
# ---------------------------------------------------------------------------
FESTIVAL_NAME_OPTIONS = [
    "None", "Back_to_School", "Baisakhi", "Bhai_Dooj", "Big_Billion_Day",
    "Bihu", "Chhath_Puja", "Christmas", "Dhanteras", "Diwali",
    "Durga_Puja", "Dussehra", "Eid_ul_Adha", "Eid_ul_Fitr", "End_of_Season_Sale_Jan",
    "End_of_Season_Sale_Jul", "Ganesh_Chaturthi", "Govardhan_Puja", "Gudi_Padwa", "Guru_Nanak_Jayanti",
    "Holi", "Independence_Day", "Janmashtami", "Karwa_Chauth", "Lohri",
    "Maha_Shivratri", "Makar_Sankranti", "Navratri", "New_Year", "Onam",
    "Pongal", "Raksha_Bandhan", "Ram_Navami", "Rath_Yatra", "Republic_Day",
    "Teej", "Ugadi", "Vasant_Panchami", "Wedding_Season_Start"
]

FESTIVAL_TYPE_OPTIONS = ["None", "Major", "Minor", "Shopping_Event"]

REGION_OPTIONS = ["None", "East", "National", "North", "South", "West"]

FESTIVAL_NAME_MAP = {
    "Back_to_School": 0, "Baisakhi": 1, "Bhai_Dooj": 2, "Big_Billion_Day": 3,
    "Bihu": 4, "Chhath_Puja": 5, "Christmas": 6, "Dhanteras": 7, "Diwali": 8,
    "Durga_Puja": 9, "Dussehra": 10, "Eid_ul_Adha": 11, "Eid_ul_Fitr": 12,
    "End_of_Season_Sale_Jan": 13, "End_of_Season_Sale_Jul": 14,
    "Ganesh_Chaturthi": 15, "Govardhan_Puja": 16, "Gudi_Padwa": 17,
    "Guru_Nanak_Jayanti": 18, "Holi": 19, "Independence_Day": 20,
    "Janmashtami": 21, "Karwa_Chauth": 22, "Lohri": 23, "Maha_Shivratri": 24,
    "Makar_Sankranti": 25, "Navratri": 26, "New_Year": 27, "Onam": 28,
    "Pongal": 29, "Raksha_Bandhan": 30, "Ram_Navami": 31, "Rath_Yatra": 32,
    "Republic_Day": 33, "Teej": 34, "Ugadi": 35, "Vasant_Panchami": 36,
    "Wedding_Season_Start": 37, "None": 38
}

FESTIVAL_TYPE_MAP = {
    "Major": 0, "Minor": 1, "Shopping_Event": 2, "None": 3
}

REGION_MAP = {
    "East": 0, "National": 1, "North": 2, "South": 3, "West": 4, "None": 5
}

WEEKDAY_MAP = {
    "Friday": 0, "Monday": 1, "Saturday": 2, "Sunday": 3, "Thursday": 4, "Tuesday": 5, "Wednesday": 6
}

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
            row.append(REGION_MAP.get(val, REGION_MAP["None"]))
        elif feat == "weekday":
            row.append(WEEKDAY_MAP.get(val, WEEKDAY_MAP["Monday"]))
        elif feat in ("is_regional_event", "is_festival_day", "pre_festival_week"):
            row.append(1.0 if val in (True, "true", "1", 1) else 0.0)
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
        X = pd.DataFrame([row], columns=FEATURE_ORDER)
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
