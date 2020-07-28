# mantis/__init__.py
from logging.config import fileConfig
from os import path

from lynx.app import *

log_file_path = path.join(path.dirname(path.abspath(__file__)), '..', 'logging_config.ini')

__all__ = [
    'create_app'
]

try:
    fileConfig(log_file_path)
except KeyError as e:
    error = str(e).strip().split('\n')[0]
    print(f'Unable to load logging configurations. Key Error: {error}')
