from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    message = fields.Str(required=True, description="Human-readable response message")


class UserRegisterSchema(Schema):
    email = fields.Email(required=True, description="Email address of the user")
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True, description="Password (min 6 chars)")


class UserLoginSchema(Schema):
    email = fields.Email(required=True, description="Email address of the user")
    password = fields.Str(required=True, load_only=True, description="Password")


class UserOutSchema(Schema):
    id = fields.Int(required=True, description="User ID")
    email = fields.Email(required=True, description="Email address")
    created_at = fields.DateTime(required=True, description="Creation timestamp")


class NoteCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255), description="Note title")
    content = fields.Str(required=False, allow_none=True, description="Note content")


class NoteUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1, max=255), description="Note title")
    content = fields.Str(required=False, allow_none=True, description="Note content")


class NoteOutSchema(Schema):
    id = fields.Int(required=True, description="Note ID")
    user_id = fields.Int(required=True, description="Owner user ID")
    title = fields.Str(required=True, description="Note title")
    content = fields.Str(allow_none=True, description="Note content")
    created_at = fields.DateTime(required=True, description="Created at")
    updated_at = fields.DateTime(required=True, description="Updated at")


class PaginatedNotesSchema(Schema):
    items = fields.List(fields.Nested(NoteOutSchema), required=True, description="List of notes")
    total = fields.Int(required=True, description="Total items")
    page = fields.Int(required=True, description="Current page")
    per_page = fields.Int(required=True, description="Items per page")
    pages = fields.Int(required=True, description="Total pages")
