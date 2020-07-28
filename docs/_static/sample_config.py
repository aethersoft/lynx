# instance/config.py

SECRET_KEY = 'secret-key'

# DEV CONFIG
POSTGRES_HOST = '127.0.0.1'
POSTGRES_POST = '5432'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'admin@123'
POSTGRES_DATABASE = 'lynx'

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
