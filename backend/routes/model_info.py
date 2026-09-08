from flask import Blueprint, jsonify

from services import prediction_service

model_info_bp = Blueprint("model_info", __name__)


@model_info_bp.route("/api/model-info", methods=["GET"])
def model_info():
    if not prediction_service.is_model_loaded():
        return jsonify({"error": "Model failed to load on server."}), 500

    return jsonify({
        "model_type": prediction_service.get_model_type_name(),
        "n_features": len(prediction_service.FEATURE_ORDER),
        "feature_names": prediction_service.FEATURE_ORDER,
        "options": prediction_service.get_options(),
    })
