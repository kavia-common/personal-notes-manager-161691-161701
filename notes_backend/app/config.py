import os
from datetime import timedelta


class Config:
    """Application configuration loaded from environment variables.

    Uses environment variables to configure the application to avoid hardcoding.
    Required variables should be set in the container environment (.env handled by orchestrator).
    """

    # Flask secret for sessions and general crypto needs (JWT uses its own secret)
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

    # Database URL for notes_database dependency; default to SQLite for local dev
    # Example for Postgres: postgresql+psycopg2://user:password@host:port/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "NOTES_DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///notes.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", str(60 * 60)))  # 1 hour default
    )

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
