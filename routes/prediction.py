from flask import Blueprint, jsonify, request

from services import prediction_service

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/api/predict", methods=["POST"])
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
    if not prediction_service.is_model_loaded():
        return jsonify({"error": "Model not loaded on server."}), 500

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Send a JSON body with all 14 fields."}), 400

    try:
        prediction, encoded_input = prediction_service.run_prediction(data)
        return jsonify({
            "prediction": prediction,
            "encoded_input": encoded_input,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
