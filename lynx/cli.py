# lynx/cli.py
import importlib
import logging
import os
import sys

import click
import psycopg2

from lynx.app import *
from lynx.shared import *

logger = logging.getLogger(__name__)

sys.path.append('..')

if os.path.exists('instance/config.py'):
    i = importlib.import_module('instance.config')
elif 'DATABASE_URL' in os.environ:
    i = importlib.import_module('config.environ')
else:
    raise FileNotFoundError('Configuration file not found.')


@click.group()
def cli():
    pass


@cli.group()
def app():
    pass


@app.command()
def start():
    create_app().run(host='0.0.0.0')


@cli.group()
def database():
    pass


@cli.group()
def admin():
    pass


@database.group()
def tables():
    pass


# noinspection PyShadowingNames
@tables.command()
@click.option('-d', '--drop', is_flag=True, default=False)
def create(drop):
    with create_app().app_context():
        if drop:
            logger.info(f'Deleting all tables in {i.POSTGRES_DATABASE}')
            db.drop_all()
            logger.info(f'Completed deleting all tables from {i.POSTGRES_DATABASE}')
        logger.info(f'Creating all tables of {i.POSTGRES_DATABASE}')
        try:
            db.create_all()
        except Exception as e:
            error = str(e).strip().split('\n')[0]
            logger.error(f'Error: {error}')
        logger.info(f'Completed creating all tables of {i.POSTGRES_DATABASE}')


@tables.command()
def drop():
    logger.info(f'Deleting all tables in {i.POSTGRES_DATABASE}')
    with create_app().app_context():
        db.drop_all()
    logger.info(f'Completed deleting all tables from {i.POSTGRES_DATABASE}')


def db_operation(op='CREATE'):
    logger.info(f'Running operation \'{op}\' for {i.POSTGRES_DATABASE}')
    # establishing the connection
    conn = psycopg2.connect(
        user=i.POSTGRES_USER, password=i.POSTGRES_PASSWORD,
        host=i.POSTGRES_HOST, port=i.POSTGRES_POST
    )
    conn.autocommit = True
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Preparing query to create a database
    sql = f'{op.upper()} database {i.POSTGRES_DATABASE}'
    # Creating a database
    try:
        cursor.execute(sql)
        logger.info(f'Completed operation \'{op}\' for {i.POSTGRES_DATABASE}')
    except psycopg2.errors.InvalidCatalogName as e:
        error = str(e).strip().split('\n')[0]
        logger.error(f'Error: {error}')
    finally:
        # Closing the connection
        conn.close()


@database.command()
def create():
    db_operation('CREATE')


@database.command()
def drop():
    db_operation('DROP')


if __name__ == '__main__':
    cli()
