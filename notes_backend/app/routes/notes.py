from typing import Optional

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from ..models import db, User, Note
from ..schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserOutSchema,
    MessageSchema,
    NoteCreateSchema,
    NoteOutSchema,
    NoteUpdateSchema,
    PaginatedNotesSchema,
)
from ..auth import create_token_for_user, jwt_required, get_current_user_id


blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api",
    description="Endpoints for user authentication and CRUD operations on notes",
)


# PUBLIC_INTERFACE
@blp.route("/auth/register")
class Register(MethodView):
    """User registration endpoint.

    Accepts email and password. Creates a new user if email not used.
    Returns a JWT access token.
    """
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserOutSchema, description="User created")
    @blp.alt_response(400, MessageSchema, description="Invalid input or email already taken")
    def post(self, payload):
        """Register a new user.

        Body:
          - email: string (email)
          - password: string (min 6)
        Returns: user details (no password) and sets up identity for future login flows.
        """
        email = payload["email"].lower().strip()
        password = payload["password"]

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Email is already registered")

        return {"id": user.id, "email": user.email, "created_at": user.created_at}


# PUBLIC_INTERFACE
@blp.route("/auth/login")
class Login(MethodView):
    """User login endpoint.

    Accepts email and password. Returns JWT token if valid.
    """
    @blp.arguments(UserLoginSchema)
    @blp.response(200, schema=MessageSchema, description="Login successful")
    @blp.alt_response(401, MessageSchema, description="Invalid credentials")
    def post(self, payload):
        """Login user and return access token."""
        email = payload["email"].lower().strip()
        password = payload["password"]

        user: Optional[User] = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            abort(401, message="Invalid email or password")

        token = create_token_for_user(user.id)
        return {"message": "Login successful", "access_token": token}


# PUBLIC_INTERFACE
@blp.route("/notes")
class NotesCollection(MethodView):
    """List and Create notes for the authenticated user."""
    @jwt_required
    @blp.response(200, PaginatedNotesSchema, description="List notes")
    def get(self):
        """List notes of the current user with pagination.

        Query params:
          - page: int (default 1)
          - per_page: int (default 10, max 100)
        """
        user_id = get_current_user_id()
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)

        query = Note.query.filter_by(user_id=user_id).order_by(Note.updated_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = pagination.items

        return {
            "items": [
                {
                    "id": n.id,
                    "user_id": n.user_id,
                    "title": n.title,
                    "content": n.content,
                    "created_at": n.created_at,
                    "updated_at": n.updated_at,
                }
                for n in items
            ],
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @jwt_required
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteOutSchema, description="Note created")
    def post(self, payload):
        """Create a new note for the current user."""
        user_id = get_current_user_id()
        note = Note(user_id=user_id, title=payload["title"], content=payload.get("content"))
        db.session.add(note)
        db.session.commit()
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }


# PUBLIC_INTERFACE
@blp.route("/notes/<int:note_id>")
class NoteItem(MethodView):
    """Retrieve, update, and delete a single note belonging to the authenticated user."""
    @jwt_required
    @blp.response(200, NoteOutSchema, description="Note details")
    @blp.alt_response(404, MessageSchema, description="Note not found")
    def get(self, note_id: int):
        """Get a single note by id."""
        user_id = get_current_user_id()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @jwt_required
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteOutSchema, description="Note updated")
    @blp.alt_response(404, MessageSchema, description="Note not found")
    def put(self, payload, note_id: int):
        """Update a note by id."""
        user_id = get_current_user_id()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")

        if "title" in payload and payload["title"] is not None:
            note.title = payload["title"]
        if "content" in payload:
            note.content = payload["content"]

        db.session.commit()
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @jwt_required
    @blp.response(204, description="Note deleted")
    @blp.alt_response(404, MessageSchema, description="Note not found")
    def delete(self, note_id: int):
        """Delete a note by id."""
        user_id = get_current_user_id()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")

        db.session.delete(note)
        db.session.commit()
        return "", 204
