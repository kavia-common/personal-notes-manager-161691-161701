from functools import wraps
from typing import Callable, Optional

from flask import jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)

jwt = JWTManager()


def create_token_for_user(user_id: int) -> str:
    """Create a JWT access token for a given user id."""
    return create_access_token(identity=str(user_id))


def jwt_required(fn: Callable):
    """Decorator to enforce JWT authentication on endpoints.

    Wraps flask_jwt_extended.verify_jwt_in_request to return consistent JSON.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"message": "Unauthorized", "error": str(e)}), 401
        return fn(*args, **kwargs)
    return wrapper


def get_current_user_id() -> Optional[int]:
    """Return the current user id from the JWT token if present, else None."""
    try:
        identity = get_jwt_identity()
        if identity is None:
            return None
        return int(identity)
    except Exception:
        return None
