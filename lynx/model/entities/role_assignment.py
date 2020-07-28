from marshmallow import Schema, fields, validate

from lynx.shared import *

__all__ = [
    'RoleAssignment',
    'RoleAssignmentSchema',
]

user_roles = ['admin', 'contributor']


class RoleAssignment(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(32), primary_key=True)


class RoleAssignmentSchema(Schema):
    project_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    user = fields.Nested('UserSchema', dump_only=True, required=True)
    role = fields.String(required=True, validate=validate.OneOf(user_roles), default=user_roles[0])

    class Meta:
        model = RoleAssignment
