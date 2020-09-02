from marshmallow import Schema, fields, validate, missing
from marshmallow.utils import get_value

from lynx.shared import *

__all__ = [
    'Project',
    'ProjectSchema',
]

scheduler_types = [
    ('Default', 'default'),
    ('Depth First', 'depth_first'),
    ('Breadth First', 'breadth_first'),
]

DEFAULT_PRESENTER = '''<div><div class="card mb-3"><div class="card-body"><p class="card-text lead">{{ document.text }}</p></div></div><div class="d-flex flex-column pb-3" v-for="(task, i) in tasks" :key="i"><div class="card"><div class="card-header"><div class="d-flex"> <span class="font-weight-bolder text-monospace">{{ task.name }}</span> <span class="ml-3 font-weight-lighter text-monospace">{{ task.description }}</span></div></div><div class="card-body"><div v-if="task.type === 'document_labeling'"><div class="custom-control custom-checkbox inline-flex" v-for="(label, j) in task.labels" :key="j"> <input class="custom-control-input" type="checkbox" v-model="annotations[task.id][label.id]" v-bind:id="'checkbox_' + task.id + '_' + label.id"> <label class="custom-control-label" v-bind:for="'checkbox_' + task.id + '_' + label.id">{{ label.label }} <span class="badge badge-light" v-if="label.shortcut"> {{ label.shortcut }} </span> </label></div></div><div v-if="task.type === 'sequence_tagging'"><div v-if="task.id in annotations" v-bind:id="'sequence_tagging_' + task.id" class="annotator-div"></div></div></div></div></div></div>'''


class Project(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    description = db.Column(db.Text())
    # How to show documents in the project to finish (breadth or depth)
    scheduler = db.Column(db.Text)
    # Project presenter (HTML)
    presenter = db.Column(db.Text)
    # Number of times each document should be annotated (maximum number of users who annotate a document)
    redundancy = db.Column(db.Integer)
    # Set project owner
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='project', lazy=True, cascade="all, delete-orphan")
    user_roles = db.relationship('UserRole', backref='project', lazy=True, cascade="all, delete-orphan")


class ProjectSchema(Schema):
    id = fields.Integer(dump_only=True, required=True)
    name = fields.String(required=True, validate=[validate.Length(min=1, max=256)])
    description = fields.String(required=True, validate=[validate.Length(min=1, max=2048)])
    presenter = fields.String(default=DEFAULT_PRESENTER)
    owner_id = fields.Integer(required=True)
    scheduler = fields.String(validate=validate.OneOf(list(zip(*scheduler_types))[1]), default=scheduler_types[0][1])
    redundancy = fields.Integer(default=3)

    @classmethod
    def get_attribute(cls, attr, obj, default):
        return get_value(attr, obj, default=default) or missing

    class Meta:
        model = Project
