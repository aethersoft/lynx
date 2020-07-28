from lynx.model.entities import *
from lynx.shared import *


def _unknown_attribute(name):
    return {
        name: ['Attribute not found.']
    }


def _object_does_not_exist():
    return {
        '_root': ['Object does not exist.']
    }


def create_object(obj, many=False, commit=True):
    assert obj is not None, _object_does_not_exist()
    try:
        if many:
            db.session.add_all(obj)
        else:
            db.session.add(obj)
        if commit:
            db.session.commit()
    except Exception as e:
        raise
    finally:
        db.session.rollback()


def update_object(obj, data, commit=True):
    assert obj is not None, _object_does_not_exist()
    try:
        for name, value in data.items():
            assert hasattr(obj, name), _unknown_attribute(name)
            setattr(obj, name, value)
        if commit:
            db.session.commit()
    except Exception as e:
        raise
    finally:
        if commit:
            db.session.rollback()


def delete_object(obj, is_query=False, commit=True):
    assert obj is not None, _object_does_not_exist()
    try:
        if is_query:
            obj.delete()
        else:
            db.session.delete(obj)
        if commit:
            db.session.commit()
    except Exception as e:
        raise
    finally:
        db.session.rollback()


def get_annotation_set(user_id, document_id):
    annotation_set = AnnotationSet.query.filter(
        AnnotationSet.user_id == user_id,
        AnnotationSet.document_id == document_id
    ).one_or_none()
    if annotation_set is None:
        schema = AnnotationSetSchema()
        data = {'user_id': user_id, 'document_id': document_id}
        data = schema.load(data)  # fill with default values
        annotation_set = AnnotationSet(**data)
        create_object(annotation_set)
    return annotation_set
