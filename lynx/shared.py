from flask_sqlalchemy import SQLAlchemy

from lynx.auth import Auth

__all__ = [
    'db',
    'auth',
]

db = SQLAlchemy()

auth = Auth()
