import os
from flask import Flask
from flask_cors import CORS
from models import init_tables
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.alerts import alerts_bp
from routes.telemetry import telemetry_bp
from routes.config import config_bp
import services.ml_service as ml_service

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'agro-intelligence-secret-2026-key')
CORS(app, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(telemetry_bp)
app.register_blueprint(config_bp)

if __name__ == '__main__':
    # Initialize DB schema if sqlite or postgresql is set up
    init_tables()
    
    # Pre-load ML models
    ml_service.load_ml_models()
    
    app.run(host='0.0.0.0', port=5000)
