from marshmallow import Schema, fields

from lynx.shared import *

__all__ = [
    'AnnotationSet',
    'AnnotationSetSchema',
]


class AnnotationSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    flagged = db.Column(db.Boolean, nullable=False, default=False)
    skipped = db.Column(db.Boolean, nullable=False, default=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # Relationships
    annotations = db.relationship('Annotation', backref='annotation_set', lazy=True, cascade="all, delete-orphan")
    db.UniqueConstraint(user_id, document_id)


class AnnotationSetSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    user_id = fields.Integer(required=True)
    document_id = fields.Integer(required=True)
    flagged = fields.Boolean(default=False)
    skipped = fields.Boolean(default=False)
    completed = fields.Boolean(default=False)
    annotations = fields.Nested('AnnotationSchema', many=True)

    class Meta:
        model = AnnotationSet
