import logging
import os
from os import path

from flask import Flask

from lynx.api import *
from lynx.shared import *

logger = logging.getLogger(__name__)

__all__ = [
    'create_app'
]


def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def create_app(config_filename=None):
    this = Flask(__name__, static_folder=path.join('..', 'static'))

    # Load the default configuration
    this.config.from_object('config.default')

    this.after_request(after_request)

    if 'DATABASE_URL' in os.environ:
        this.config.from_pyfile('../config/environ.py')
    elif os.path.exists('instance/config.py'):
        # Load the configuration from the instance folder
        this.config.from_pyfile('../instance/config.py')
    else:
        raise FileNotFoundError('Configuration file not found.')

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    if 'APP_CONFIG_FILE' in os.environ:
        this.config.from_envvar('APP_CONFIG_FILE')

    this.register_blueprint(api_blueprint, url_prefix=api_blueprint.url_prefix)

    db.init_app(this)

    return this
