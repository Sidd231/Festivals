from flask import Blueprint, jsonify

from services import prediction_service

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "Backend is running",
        "model_loaded": prediction_service.is_model_loaded(),
    })
