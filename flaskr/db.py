import sqlite3
from datetime import datetime

import click
from flask import current_app, g, Flask

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #tells connection to return rows that behave like dicts

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():

    init_db()
    click.echo('db initialized')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode()) #tells python how to interpret timestamp values, converting value to datetime.datetime
)

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) #adds new command that can be called with flask command
    