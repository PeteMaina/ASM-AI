
from flask import Flask
from backend.routes import routes_bp
from backend.auth import auth_bp
from backend.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(routes_bp, url_prefix="/api")

    return app
