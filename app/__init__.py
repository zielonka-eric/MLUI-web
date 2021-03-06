from flask import Flask, g
import sqlite3
import logging

app = Flask(__name__)

#set up database connection
# ( from http://flask.pocoo.org/docs/1.0/patterns/sqlite3/ )
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect('database.db', isolation_level=None)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app.logger.setLevel(logging.INFO)
#app.logger.setLevel(logging.DEBUG)

from app import routes