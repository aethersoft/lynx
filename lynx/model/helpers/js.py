__all__ = [
    'success',
    'fail',
    'error',
]


def success(data=None):
    return {
        'data': data,
        'status': 'success',
    }


def fail(data=None):
    return {
        'data': data,
        'status': 'fail',
    }


def error(message='Server Error. Please contact admin to resolve the issue.', data=None):
    return {
        'message': message,
        'data': data,
        'code': 500,
        'status': 'error',
    }
