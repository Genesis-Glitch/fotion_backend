from flask import Flask, current_app
from flask import Flask, render_template
import json

from db import get_db

app = Flask(__name__)

@app.route('/initdb')
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/<name>', methods = ['GET'])
def get_username(name):
    return name

@app.route('/events', methods = ['GET'])
def get_events():
    conn = get_db()
    events = conn.execute('SELECT title, body FROM event').fetchall()
    conn.close()

    results = [tuple(row) for row in events]

    return json.dumps(results)


if __name__ == '__main__':
    app.run()
