# instance/config.py

import os
from urllib.parse import urlparse

SECRET_KEY = 'secret-key'

o = urlparse(os.environ['DATABASE_URL'])

POSTGRES_HOST = o.hostname
POSTGRES_POST = o.port
POSTGRES_USER = o.username
POSTGRES_PASSWORD = o.password
POSTGRES_DATABASE = o.path[1:]

# noinspection SpellCheckingInspection
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}'.format(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    hostname=POSTGRES_HOST,
    port=POSTGRES_POST,
    database=POSTGRES_DATABASE
)

# noinspection SpellCheckingInspection
SQLALCHEMY_TRACK_MODIFICATIONS = False
