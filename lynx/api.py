import json

from flask import Blueprint, request, g
from flask_restful import Resource, Api
from flask_restful_swagger import swagger
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import func, and_, or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash as hash_password, check_password_hash

from lynx import utils
from lynx.model.entities import *
from lynx.model.helpers import js, eg, op
from lynx.shared import *

__all__ = [
    'api_blueprint'
]

api_blueprint = Blueprint('api', __name__, template_folder='templates')

api_blueprint.version = 1
api_blueprint.url_prefix = f'/api/v{api_blueprint.version}'
api_blueprint.config = {}


# noinspection PyMethodMayBeStatic
class RestfulAPI(Api):
    def handle_error(self, e):
        if isinstance(e, ValidationError):
            return js.fail(data=e.messages)
        if isinstance(e, AssertionError) and len(e.args) > 0:
            return js.fail(data=e.args[0])
        if isinstance(e, TypeError):
            return js.fail(data={'_root': [str(e)]})
        if isinstance(e, IntegrityError):
            return js.fail(data={'_root': [e.args]})
        return js.error(
            data={
                '_root': ['We found an error in the server. Please contact your administrator to resolve the issue.']},
            message=str(e)
        )


restful = RestfulAPI(api_blueprint)

api = swagger.docs(
    restful,
    apiVersion=f'{api_blueprint.version}',
    api_spec_url='/swagger',
    description='Documents all public API endpoints.'
)


def auth_error(status=401):
    return js.error('Access Denied', {'auth': [f'Access Denied {status}']}), status


@api_blueprint.record
def record_params(setup_state):
    app = setup_state.app
    api.config = dict([(key, value) for (key, value) in app.config.items()])
    app.config['API_VERSION'] = api_blueprint.version
    app.config['API_URL_PREFIX'] = api_blueprint.url_prefix
    token_auth.error_handler(auth_error)
    basic_auth.error_handler(auth_error)


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False
    g.current_user = user
    return True


def generate_token(user, expiration=3600):
    s = Serializer(api.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user.id})


@token_auth.verify_token
def verify_token(token):
    s = Serializer(api.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    user = User.query.get(data['id'])
    g.current_user = user
    return True


# noinspection PyMethodMayBeStatic
@swagger.model
class TokenEndpoint(Resource):
    @swagger.operation(
        notes='Retrieve token.',
        nickname='retrieve_token',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self):
        check = bool(request.args.get('check', False))
        if check:
            return js.success()
        token = generate_token(g.current_user)
        user_schema = UserSchema()
        current_user = user_schema.dump(g.current_user)
        return js.success({'token': token.decode('ascii'), 'user': current_user})


# noinspection PyMethodMayBeStatic
@swagger.model
class ProjectsEndpoint(Resource):
    @swagger.operation(
        notes='Retrieve all projects.',
        nickname='retrieve_projects',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self):
        offset = request.args.get('offset', None)
        limit = request.args.get('limit', None)
        user_id = g.current_user.id
        query = Project.query \
            .join(RoleAssignment, RoleAssignment.project_id == Project.id) \
            .filter(and_(RoleAssignment.user_id == user_id, RoleAssignment.role == 'admin'))
        paginate = utils.paginate(query, limit, offset)
        data = ProjectSchema().dump(paginate.items, many=True)
        return js.success({
            'pagination': {
                'page': paginate.page,
                'pages': paginate.pages,
                'has_prev': paginate.has_prev,
                'has_next': paginate.has_next,
                'per_page': paginate.per_page,
                'total': paginate.total,
                'items': data,
            },
        })

    @swagger.operation(
        notes='Creates project with provided data.',
        nickname='create_projects',
        parameters=[
            {
                "name": "project",
                "description": f'Project to Import. <br> Example: {eg.project}',
                "required": True,
                "allowMultiple": False,
                "dataType": Project.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    @auth.login_required
    def post(self):
        data = request.get_json()
        schema = ProjectSchema()
        data = schema.load(data, unknown=EXCLUDE)
        project = Project(**data)
        # Create project (do not commit)
        op.create_object(project, commit=False)
        data = {
            'project': project,
            'user_id': g.current_user.id,
            'role': 'admin'
        }
        role_assignment = RoleAssignment(**data)
        op.create_object(role_assignment)
        data = schema.dump(project)
        return js.success(data)


# noinspection PyMethodMayBeStatic
@swagger.model
class ProjectByIDEndpoint(Resource):
    @swagger.operation(
        notes='Retrieve project with provided ID.',
        nickname='retrieve_project',
        parameters=[],
        responseMessages=[],
    )
    def get(self, project_id):
        project = Project.query.get(project_id)
        data = ProjectSchema().dump(project)
        return js.success(data)

    @swagger.operation(
        notes='Updates project with provided data.',
        nickname='update_projects',
        parameters=[{
            "name": "project",
            "description": f'Project to Update. <br> Example: {eg.project}',
            "required": True,
            "allowMultiple": False,
            "dataType": Project.__name__,
            "paramType": "body",
        }],
        responseMessages=[],
    )
    @auth.login_required
    def put(self, project_id):
        data = request.get_json()
        schema = ProjectSchema()
        schema.load(data, partial=True, unknown=EXCLUDE)
        project = Project.query.get(project_id)
        op.update_object(project, data)
        data = schema.dump(project)
        return js.success(data)

    @swagger.operation(
        notes='Deletes project with provided project ID.',
        nickname='delete_projects',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def delete(self, project_id):
        project = Project.query.get(project_id)
        op.delete_object(project)
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class DocumentsEndpoint(Resource):
    @swagger.operation(
        notes='Gets documents belonging to a project.',
        nickname='retrieve_documents',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id):
        offset = request.args.get('offset', None)
        limit = request.args.get('limit', None)
        query = Document.query.filter_by(project_id=project_id)
        paginate = utils.paginate(query, limit, offset)
        data = DocumentSchema().dump(paginate.items, many=True)
        return js.success({
            'pagination': {
                'page': paginate.page,
                'pages': paginate.pages,
                'has_prev': paginate.has_prev,
                'has_next': paginate.has_next,
                'per_page': paginate.per_page,
                'total': paginate.total,
                'items': data,
            },
        })

    @swagger.operation(
        notes='Creates document with provided data.',
        nickname='create_documents',
        parameters=[
            {
                "name": "document",
                "description": f'Document to Import. '
                               f'<br> Example 1: {eg.document} '
                               f'<br> or '
                               f'<br> Example 2: {eg.document_many}',
                "required": True,
                "allowMultiple": True,
                "dataType": Document.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    @auth.login_required
    def post(self, project_id):
        if 'file' in request.files:
            file = request.files['file']
            payload = self.process_file(file)
        else:
            payload = request.get_json()
        if isinstance(payload, list):
            for d in payload:
                d.update({'project_id': project_id})
            data = DocumentSchema().load(payload, many=True, unknown=EXCLUDE)
            documents = [Document(**d) for d in data]
            op.create_object(documents, many=True)
        else:
            payload.update({'project_id': project_id})
            data = DocumentSchema().load(payload, unknown=EXCLUDE)
            document = Document(**data)
            op.create_object(document)
        return js.success()

    def process_file(self, file):
        if file and file.filename.endswith('json'):
            data = file.read().decode(api.config.get('ENCODING', 'utf-8'))
            try:
                documents = json.loads(data.strip())
            except json.decoder.JSONDecodeError:
                # Try each-line-json format
                documents = []
                skipped = []
                for line in data.split('\n'):
                    try:
                        documents.append(json.loads(line.strip()))
                    except json.decoder.JSONDecodeError:
                        skipped += line
            return documents
        return []


# noinspection PyMethodMayBeStatic
@swagger.model
class DocumentByIDEndpoint(Resource):
    @swagger.operation(
        notes='Updates document with provided data.',
        nickname='update_document',
        parameters=[{
            "name": "project",
            "description": f'Document to Update. <br> Example: {eg.document}',
            "required": True,
            "allowMultiple": False,
            "dataType": Document.__name__,
            "paramType": "body",
        }],
        responseMessages=[],
    )
    @auth.login_required
    def put(self, project_id, document_id):
        data = request.get_json()
        document = Document.query.get(document_id)
        op.update_object(document, data)
        data = DocumentSchema().dump(document)
        return js.success(data)

    @swagger.operation(
        notes='Deletes document with provided document ID.',
        nickname='delete_document',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def delete(self, project_id, document_id):
        document = Document.query.get(document_id)
        op.delete_object(document)
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class TasksEndpoint(Resource):
    @swagger.operation(
        notes='Gets tasks belonging to a project.',
        nickname='retrieve_tasks',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id):
        tasks = Task.query.filter_by(project_id=project_id).all()
        data = TaskSchema().dump(tasks, many=True)
        return js.success(data)

    @swagger.operation(
        notes='Creates task with provided data.',
        nickname='create_tasks',
        parameters=[
            {
                "name": "task",
                "description": f'Task to Import. <br> Example: {eg.task}',
                "required": True,
                "allowMultiple": False,
                "dataType": Task.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    @auth.login_required
    def post(self, project_id):
        data = request.get_json()
        data.update({'project_id': project_id})
        labels = utils.iferror(lambda: data['labels'], [])
        schema = TaskSchema()
        data = schema.load(data, unknown=EXCLUDE)
        task = Task(**data)
        task.labels[:] = []
        for label_data in labels:
            label = None
            if 'id' in label_data:
                label_id = label_data['id']
                label = Label.query.get(label_id)
            if label is None:  # create if label not found
                label_schema = LabelSchema()
                label_data = label_schema.load(label_data)
                label = Label(**label_data)
            task.labels.append(label)
        op.create_object(task)
        data = schema.dump(task)
        return js.success(data)


# noinspection PyMethodMayBeStatic
@swagger.model
class TaskByIDEndpoint(Resource):
    @swagger.operation(
        notes='Gets task with provided task id.',
        nickname='retrieve_task',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id, task_id):
        task = Task.query.get(task_id)
        data = TaskSchema().dump(task)
        return js.success(data)

    @swagger.operation(
        notes='Updates task with provided data.',
        nickname='update_task',
        parameters=[{
            "name": "task",
            "description": f'Task to Update. <br> Example: {eg.task}',
            "required": True,
            "allowMultiple": False,
            "dataType": Task.__name__,
            "paramType": "body",
        }],
        responseMessages=[],
    )
    @auth.login_required
    def put(self, project_id, task_id):
        data = request.get_json()
        data.update({'project_id': project_id})
        schema = TaskSchema()
        data_labels = data['labels']
        data = schema.load(data, unknown=EXCLUDE)
        task = Task.query.get(task_id)
        task.labels[:] = []
        for data_label in data_labels:
            label = None
            if 'id' in data_label:
                label_id = data_label['id']
                label = Label.query.get(label_id)
            if label is None:  # create if label not found
                label_schema = LabelSchema()
                data_label = label_schema.load(data_label)
                label = Label(**data_label)
            else:
                op.update_object(label, data_label, commit=False)
            task.labels.append(label)
        op.update_object(task, data)
        data = schema.dump(task)
        return js.success(data)

    @swagger.operation(
        notes='Deletes task with provided task ID.',
        nickname='delete_task',
        parameters=[],
        responseMessages=[],
    )
    def delete(self, project_id, task_id):
        task = Task.query.get(task_id)
        op.delete_object(task)
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class UsersEndpoint(Resource):
    @swagger.operation(
        notes='Gets users in the system.',
        nickname='retrieve_users',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self):
        search = None
        if 'q' in request.args:
            search = request.args.get('q')
        query = User.query
        if search is not None:
            query = query.filter(User.username.contains(search))
        users = query.all()
        data = UserSchema().dump(users, many=True)
        return js.success(data)

    @swagger.operation(
        notes='Creates user with provided data.',
        nickname='create_user',
        parameters=[
            {
                "name": "user",
                "description": f'User to Import. <br> Example: {eg.user}',
                "required": True,
                "allowMultiple": False,
                "dataType": User.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    def post(self):
        payload = request.get_json()
        schema = UserSchema()
        data = schema.load(payload, unknown=EXCLUDE)
        if 'password' in data:
            data['password'] = hash_password(data['password'])
        user = User(**data)
        assert User.query.filter_by(username=user.username).count() == 0, {
            '_root': ['Username already exists in the system. Please try another username.']
        }
        op.create_object(user)
        data = schema.dump(user)
        return js.success(data)


# noinspection PyMethodMayBeStatic
@swagger.model
class UserByIDEndpoint(Resource):
    @swagger.operation(
        notes='Updates user with provided data.',
        nickname='update_user',
        parameters=[{
            "name": "user",
            "description": f'User to Update. <br> Example: {eg.user}',
            "required": True,
            "allowMultiple": False,
            "dataType": User.__name__,
            "paramType": "body",
        }],
        responseMessages=[],
    )
    @auth.login_required
    def put(self, user_id):
        payload = request.get_json()
        schema = UserSchema()
        data = schema.load(payload, unknown=EXCLUDE)
        if 'password' in data:
            data['password'] = hash_password(data['password'])
        user = User.query.get(user_id)
        op.update_object(user, data)
        data = schema.dump(user)
        return js.success(data)

    @swagger.operation(
        notes='Deletes user with provided user ID.',
        nickname='delete_user',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        op.delete_object(user)
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class RoleAssignmentsEndpoint(Resource):
    @swagger.operation(
        notes='Gets role assignments of all users for a provided project.',
        nickname='retrieve_roles',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id):
        user_roles = RoleAssignment.query.filter_by(project_id=project_id).all()
        data = RoleAssignmentSchema().dump(user_roles, many=True)
        return js.success(data)

    @swagger.operation(
        notes='Add user with provided role to provided project.',
        nickname='create_roles',
        parameters=[
            {
                "name": "user",
                "description": f'Adds role assignment to project. <br> Example: {eg.user_roles}',
                "required": True,
                "allowMultiple": False,
                "dataType": User.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    @auth.login_required
    def post(self, project_id):
        payload = request.get_json()
        # get user id
        assert 'username' in payload, {'username': [
            'Required field \'username\' not found.'
        ]}
        username = payload['username']
        user = User.query.filter_by(username=username).first()
        assert user is not None, {'_root': [
            'No such user in the system.'
        ]}
        payload.update({'user_id': user.id, 'project_id': project_id})
        schema = RoleAssignmentSchema()
        data = schema.load(payload, unknown=EXCLUDE)
        role_assignment = RoleAssignment(**data)
        op.create_object(role_assignment)
        data = schema.dump(role_assignment)
        return js.success(data)

    @swagger.operation(
        notes='Deletes role for user ID.',
        nickname='delete_roles',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def delete(self, project_id):
        payload = request.get_json()
        # get user id
        assert 'username' in payload, {'username': [
            'Required field \'username\' not found.'
        ]}
        username = payload['username']
        user = User.query.filter_by(username=username).first()
        assert user is not None, {'_root': [
            'No such user in the system.'
        ]}
        # get user role to delete
        assert 'role' in payload, {'role': [
            'Required field \'role\' not found.'
        ]}
        role = payload['role']
        role = RoleAssignment.query.filter_by(project_id=project_id, user_id=user.id, role=role).first()
        op.delete_object(role)
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class AnnotateProjectsByIDEndpoint(Resource):
    @swagger.operation(
        notes='Returns <b>a [not completed] document</b> of the specified project for annotation by the logged in user.',
        nickname='retrieve_document_next',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id):
        user_id = g.current_user.id
        # Gets a document not contributed
        # :: Looks for not completed documents in projects assigned to user
        subquery = db.session.query(AnnotationSet.document_id, func.count(AnnotationSet.user_id).label('frequency')) \
            .group_by(AnnotationSet.document_id) \
            .subquery()
        document = Document.query \
            .filter_by(project_id=project_id) \
            .join(Project, Project.id == Document.project_id) \
            .outerjoin(subquery, Document.id == subquery.c.document_id) \
            .filter(or_(subquery.c.frequency.is_(None), Project.redundancy > subquery.c.frequency)) \
            .join(RoleAssignment, RoleAssignment.project_id == Project.id) \
            .filter(RoleAssignment.user_id == user_id) \
            .outerjoin(AnnotationSet, and_(AnnotationSet.document_id == Document.id,
                                           AnnotationSet.user_id == RoleAssignment.user_id), ) \
            .filter(and_(or_(AnnotationSet.completed.is_(None), AnnotationSet.completed.is_(False)),
                         or_(AnnotationSet.skipped.is_(None), AnnotationSet.skipped.is_(False)))) \
            .first()
        if document is not None:
            document_data = DocumentSchema().dump(document)
            document_data['project'] = ProjectSchema().dump(document.project)
            document_data['project']['tasks'] = TaskSchema().dump(document.project.tasks, many=True)
            annotation_set = op.get_annotation_set(user_id, document.id)
            annotation_set_data = AnnotationSetSchema().dump(annotation_set)
            return js.success({
                'document': document_data,
                'annotation_set': annotation_set_data
            })
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class AnnotateEndpoint(Resource):
    @swagger.operation(
        notes='Processes operation requested by post for a stated document in the data.',
        nickname='process_annotation_operation',
        parameters=[
            {
                "name": "operation+data",
                "description": 'Defines annotation operation.',
                "required": True,
                "allowMultiple": False,
                "dataType": 'Action',
                "paramType": "body",
            }
        ],
        responseMessages=[],
    )
    @auth.login_required
    def post(self):
        user_id = g.current_user.id
        payload = request.get_json()
        assert 'operation' in payload, {'operation': [
            'Operation not defined.'
        ]}
        operation = payload['operation']
        assert operation in ['flag', 'skip', 'save', 'next'], {'operation': [
            f'Invalid operation. Expected one of (\'flag\', \'skip\', \'save\', \'next\') found {operation}.'
        ]}
        data = payload.get('data', {})
        assert 'document_id' in data, {'document_id': [
            'Missing Attribute.'
        ]}
        data['user_id'] = user_id
        if operation == 'flag':
            return self.flag_document(data)
        elif operation == 'skip':
            return self.skip_document(data)
        else:
            return self.save_document(data)

    def flag_document(self, data):
        user_id, document_id = data['user_id'], data['document_id']
        annotation_set = op.get_annotation_set(user_id, document_id)
        op.update_object(annotation_set, {'flagged': not annotation_set.flagged})
        data = AnnotationSetSchema().dump(annotation_set)
        return js.success(data)

    def skip_document(self, data):
        user_id, document_id = data['user_id'], data['document_id']
        annotation_set = op.get_annotation_set(user_id, document_id)
        op.update_object(annotation_set, {'skipped': True})
        data = AnnotationSetSchema().dump(annotation_set)
        return js.success(data)

    def save_document(self, data):
        user_id, document_id, annotations = data['user_id'], data['document_id'], data['annotations']
        # Delete existing annotations
        annotation_set = op.get_annotation_set(user_id, document_id)
        query = Annotation.query.filter_by(annotation_set_id=annotation_set.id)
        op.delete_object(query, True)
        # Create new annotations
        schema = AnnotationSchema()
        for a in annotations:
            a['annotation_set_id'] = annotation_set.id
        data = schema.load(annotations, many=True)
        annotations = []
        for a in data:
            span = None
            if 'span' in a:
                s = a.pop('span')
                span = AnnotationSpan(**s)
            a = Annotation(**a)
            a.span = span
            annotations.append(a)
        op.create_object(annotations, many=True)
        op.update_object(annotation_set, {'completed': True})
        return js.success()


# noinspection PyMethodMayBeStatic
@swagger.model
class AnnotateProjectsEndpoint(Resource):
    @swagger.operation(
        notes='Retrieve all projects assigned to current user.',
        nickname='retrieve_annotation_projects',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self):
        offset = request.args.get('offset', 1)
        limit = request.args.get('limit', 20)
        user_id = g.current_user.id
        schema = ProjectSchema()
        query = Project.query \
            .join(RoleAssignment, RoleAssignment.project_id == Project.id) \
            .filter(and_(RoleAssignment.user_id == user_id))
        paginate = utils.paginate(query, limit, offset)
        data = schema.dump(paginate.items, many=True)
        return js.success({
            'pagination': {
                'page': paginate.page,
                'pages': paginate.pages,
                'has_prev': paginate.has_prev,
                'has_next': paginate.has_next,
                'per_page': paginate.per_page,
                'total': paginate.total,
                'items': data,
            },
        })


# noinspection PyMethodMayBeStatic
@swagger.model
class AnnotateDocumentsEndpoint(Resource):
    @swagger.operation(
        notes='Returns Annotation Set and related documents belonging to provided project for user.',
        nickname='retrieve_annotation_sets',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id):
        user_id = g.current_user.id
        try:
            offset = int(request.args.get('offset', 1))
        except ValueError as _:
            offset = 1
        try:
            limit = int(request.args.get('limit', 20))
        except ValueError as _:
            limit = 20
        query = db.session.query(Document, AnnotationSet) \
            .outerjoin(AnnotationSet, AnnotationSet.document_id == Document.id) \
            .join(Project, Project.id == Document.project_id) \
            .join(RoleAssignment, RoleAssignment.project_id == Project.id) \
            .filter(and_(RoleAssignment.user_id == user_id, Document.project_id == project_id))
        # Filter by flagged options
        var = request.args.get('flagged', None)
        if var != 'none':
            if isinstance(var, str):
                var = var == 'true'
            else:
                var = bool(var)
            query = query.filter(AnnotationSet.flagged.is_(var))
        # Filter by status options
        status = request.args.get('status', None)
        if status == 'completed':
            query = query.filter(AnnotationSet.completed.is_(True))
        elif status == 'skipped':
            query = query.filter(AnnotationSet.skipped.is_(True))
        elif status == 'active':
            query = query.filter(or_(AnnotationSet.id.is_(None), AnnotationSet.completed.is_(False)))
        paginate = utils.paginate(query, limit, offset)
        # update structure
        items = []
        for doc, annotation_set in paginate.items:
            data = DocumentSchema().dump(doc)
            data.update({'annotation_set': AnnotationSetSchema().dump(annotation_set)})
            items.append(data)
        return js.success({
            'pagination': {
                'page': paginate.page,
                'pages': paginate.pages,
                'has_prev': paginate.has_prev,
                'has_next': paginate.has_next,
                'per_page': paginate.per_page,
                'total': paginate.total,
                'items': items,
            },
        })


# noinspection PyMethodMayBeStatic
@swagger.model
class AnnotateDocumentsByIDEndpoint(Resource):
    @swagger.operation(
        notes='Retrieve annotation for document provided.',
        nickname='retrieve_annotation_document',
        parameters=[],
        responseMessages=[],
    )
    @auth.login_required
    def get(self, project_id, document_id):
        user_id = g.current_user.id
        document = Document.query.get(document_id)
        assert document is not None, {'_root': ['Document not found.']}
        document_data = DocumentSchema().dump(document)
        document_data['project'] = ProjectSchema().dump(document.project)
        document_data['project']['tasks'] = TaskSchema().dump(document.project.tasks, many=True)
        annotation_set = op.get_annotation_set(user_id, document.id)
        annotation_set_data = AnnotationSetSchema().dump(annotation_set)
        data = {'document': document_data, 'annotation_set': annotation_set_data}
        return js.success(data)


# Entity Endpoints
api.add_resource(TokenEndpoint, '/token')
api.add_resource(ProjectsEndpoint, '/projects')
api.add_resource(ProjectByIDEndpoint, '/projects/<int:project_id>')
api.add_resource(DocumentsEndpoint, '/projects/<int:project_id>/documents')
api.add_resource(DocumentByIDEndpoint, '/projects/<int:project_id>/documents/<int:document_id>')
api.add_resource(TasksEndpoint, '/projects/<int:project_id>/tasks')
api.add_resource(TaskByIDEndpoint, '/projects/<int:project_id>/tasks/<int:task_id>')
api.add_resource(UsersEndpoint, '/users')
api.add_resource(UserByIDEndpoint, '/users/<int:user_id>')
api.add_resource(RoleAssignmentsEndpoint, '/projects/<int:project_id>/users')
# Annotation Action Endpoints
api.add_resource(AnnotateEndpoint, '/annotate')
api.add_resource(AnnotateProjectsEndpoint, '/annotate/projects')
api.add_resource(AnnotateProjectsByIDEndpoint, '/annotate/projects/<int:project_id>')
api.add_resource(AnnotateDocumentsEndpoint, '/annotate/projects/<int:project_id>/documents')
api.add_resource(AnnotateDocumentsByIDEndpoint, '/annotate/projects/<int:project_id>/documents/<int:document_id>')
