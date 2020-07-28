from flask_httpauth import HTTPTokenAuth, MultiAuth, HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

__all__ = [
    'db',
    'auth',
    'basic_auth',
    'token_auth',
]

db = SQLAlchemy()

basic_auth = HTTPBasicAuth()

token_auth = HTTPTokenAuth()

auth = MultiAuth(basic_auth, token_auth)
