"""
Backend for the Festive-Aware Demand Forecast Model (XGBoost)
---------------------------------------------------------------
Thin app factory: loads config, enables CORS, registers routes.

All model/encoder loading and prediction logic lives in
services/prediction_service.py (single source of truth) and is
imported, unchanged in behavior, by the route blueprints in routes/.

SETUP (on your own machine):
    pip install -r requirements.txt

RUN:
    cd backend
    python app.py

Server starts at http://127.0.0.1:5000
"""

import os
import sys

# Allow `from services...` / `from routes...` imports regardless of the
# directory this script is invoked from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS

from routes.health import health_bp
from routes.model_info import model_info_bp
from routes.prediction import prediction_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(model_info_bp)
    app.register_blueprint(prediction_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
