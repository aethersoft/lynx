from datetime import datetime

from marshmallow import Schema, fields

from lynx.shared import *

__all__ = [
    'AnnotationSpan',
    'AnnotationSpanSchema',
    'Annotation',
    'AnnotationSchema',
]


class AnnotationSpan(db.Model):
    annotation_id = db.Column(db.Integer, db.ForeignKey('annotation.id', ondelete='CASCADE'), primary_key=True)
    start = db.Column(db.Integer)
    length = db.Column(db.Integer)


class AnnotationSpanSchema(Schema):
    annotation_id = fields.Integer(required=True, dump_only=True)
    start = fields.Integer(required=True)
    length = fields.Integer(required=True)

    class Meta:
        model = AnnotationSpan


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    annotation_set_id = db.Column(db.Integer, db.ForeignKey('annotation_set.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)
    label_id = db.Column('label_id', db.Integer, db.ForeignKey('label.id'))
    span = db.relationship('AnnotationSpan', uselist=False, backref='annotation', lazy=True, passive_deletes=True,
                           cascade="all, delete-orphan")


class AnnotationSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    timestamp = fields.DateTime()
    annotation_set_id = fields.Integer(required=True)
    task_id = fields.Integer(required=True)
    label_id = fields.Integer(required=True)
    text = fields.String(required=False)
    span = fields.Nested('AnnotationSpanSchema', many=False, required=False)
    label = fields.Nested('LabelSchema', dump_only=True, required=False)

    class Meta:
        model = Annotation
