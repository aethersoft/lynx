from marshmallow import Schema, fields, validate

from lynx.shared import *

__all__ = [
    'User',
    'UserSchema',
]


class User(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    # Relationships
    projects = db.relationship('RoleAssignment', backref='user', lazy=True)
    annotation_sets = db.relationship('AnnotationSet', backref='user', lazy=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    username = fields.String(required=True, validate=[validate.Length(min=1, max=64)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(min=8, max=32)])
    first_name = fields.String(validate=[validate.Length(min=1, max=64)])
    last_name = fields.String(validate=[validate.Length(min=1, max=64)])
    email = fields.String(validate=[validate.Length(min=0, max=64)], allow_none=True)

    class Meta:
        model = User
