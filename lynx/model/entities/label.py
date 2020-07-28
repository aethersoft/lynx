from marshmallow import Schema, fields, INCLUDE

from lynx.shared import *

__all__ = [
    'Label',
    'LabelSchema',
]


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    properties = db.Column(db.JSON, default={})
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


class LabelSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    label = fields.String(required=True)
    properties = fields.Dict(required=False)
    task_id = fields.Integer(dump_only=True, required=False)

    class Meta:
        model = Label
        unknown = INCLUDE
