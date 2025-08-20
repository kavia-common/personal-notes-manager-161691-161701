from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .config import Config
from .models import db
from .auth import jwt as jwt_manager
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Application factory for the Flask app.

    Configures CORS, OpenAPI, SQLAlchemy, JWT, and registers blueprints.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration
    app.config.from_object(Config)

    # CORS
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # OpenAPI / Swagger configuration
    app.config["API_TITLE"] = "Notes API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Initialize extensions
    db.init_app(app)
    jwt_manager.init_app(app)

    # Create tables if they do not exist (simple bootstrap)
    with app.app_context():
        db.create_all()

    # API with flask-smorest
    api = Api(app)
    api.register_blueprint(health_blp)
    api.register_blueprint(notes_blp)

    return app


# Keep a default app instance for compatibility with run.py
app = create_app()
