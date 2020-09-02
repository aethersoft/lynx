from marshmallow import Schema, fields, validate

from lynx.shared import *

__all__ = [
    'UserRole',
    'UserRoleSchema',
]

user_roles = ['admin', 'coder']


class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    role = db.Column(db.String(32))


class UserRoleSchema(Schema):
    project_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    user = fields.Nested('UserSchema', dump_only=True, required=True)
    role = fields.String(required=True, validate=validate.OneOf(user_roles), default=user_roles[0])

    class Meta:
        model = UserRole
