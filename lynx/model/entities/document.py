from marshmallow import Schema, fields

from lynx.shared import *

__all__ = [
    'Document',
    'DocumentSchema',
]


class Document(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), index=True)
    meta = db.Column(db.JSON, default={})
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # Relationships
    annotation_sets = db.relationship('AnnotationSet', backref='document', lazy=True, cascade="all, delete-orphan")


class DocumentSchema(Schema):
    id = fields.Integer(dump_only=True, required=False)
    text = fields.String(required=True)
    meta = fields.Dict(required=True)
    project_id = fields.Integer(required=True)
