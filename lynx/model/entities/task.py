from marshmallow import Schema, fields, validate

from lynx.shared import *

__all__ = [
    'Task',
    'TaskSchema',
]

task_types = [
    ('document_labeling', 'Document Labeling'),
    ('sequence_tagging', 'Sequence Tagging'),
    ('text_to_text', 'Text to Text'),
]


class Task(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    type = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    # Relationships
    labels = db.relationship('Label', backref='task', lazy=True, cascade="all, delete-orphan")
    annotations = db.relationship('Annotation', backref='task', lazy=True)


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    type = fields.String(
        validate=validate.OneOf(list(zip(*task_types))[0]),
        default=task_types[0][0]
    )
    project_id = fields.Integer(load_only=True)
    labels = fields.Nested('LabelSchema', dump_only=True, many=True, required=True, default=[])

    class Meta:
        model = Task
