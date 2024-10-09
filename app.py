from uuid import uuid4

from flask import Flask, current_app, request
from flask import Flask, render_template
import json
import agent_integration

from db import get_db

app = Flask(__name__)

@app.route('/initdb')
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    for i in range(1,10):
        print(i)
        db.execute("INSERT INTO event (id, "
                   "author_id, "
                   "created, "
                   "title, "
                   "body, "
                   "location_id, "
                   "event_date, "
                   "event_time_start, "
                   "event_time_end, "
                   "event_longitude, "
                   "event_latitude, "
                   "event_image_url) "
                   "VALUES("
                   ""+str(i)+", 1, CURRENT_TIMESTAMP, 'AUCKLAND', 'AUCKLAND FREE FOOD', 0, CURRENT_TIMESTAMP, '12:00', '13:00', '123', '321', 'https://picsum.photos/100/200');")
        db.commit()

    for i in range(11,20):
        print(i)
        db.execute("INSERT INTO event (id, "
                   "author_id, "
                   "created, "
                   "title, "
                   "body, "
                   "location_id, "
                   "event_date, "
                   "event_time_start, "
                   "event_time_end, "
                   "event_longitude, "
                   "event_latitude, "
                   "event_image_url) "
                   "VALUES("
                   ""+str(i)+", 1, CURRENT_TIMESTAMP, 'CANTERBURY', 'CANTERBURY FREE FOOD', 0, CURRENT_TIMESTAMP, '12:00', '13:00', '123', '321', 'https://picsum.photos/100/200');")
        db.commit()

    db.close()

    return "Finished"

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/<name>', methods = ['GET'])
def get_username(name):
    return name

@app.route('/event/<id>', methods = ['GET'])
def get_event(id):
    conn = get_db()
    event = conn.execute("SELECT * FROM event WHERE id = ?", (id,))

    data = ""
    for row in event:
        data = {
            "rc": "0000",
            "message": "Success",
            "data": {
                "id": row[0],
                "title": row[1],
                "description": row['body'],
                "location": "event location",
                "quota": 99,
                "event_date": "2024-12-12",
                "event_time_start": "08:00",
                "event_time_end": "15:00",
                "event_longitude": "123123123",
                "event_latitude": "234234234",
                "event_image_url": [
                    "https://picsum.photos/100/200",
                    "https://picsum.photos/100/200",
                    "https://picsum.photos/100/200",
                    "https://picsum.photos/100/200",
                    "https://picsum.photos/100/200"
                ]
            }
        }

    conn.close()

    return json.dumps(data)


@app.route("/q1")
def question1():
    event = {
        "sessionId": "MYSESSION",
        "question": prompt
    }
    resp = agent_integration.lambda_handler(event, None)

    return resp;

@app.route("/register-event")
def register_event():

    body = request.json
    print(body)

    return "";


@app.route('/events', methods = ['GET'])
def get_events():
    conn = get_db()
    events = conn.execute('SELECT id, title, body FROM event').fetchall()
    conn.close()

    results = [tuple(row) for row in events]

    datax = []
    for row in events:

        event_loc = {
             "id": str(row[0]),
             "title": row[1],
             "description": row[2],
             "location": row[1],
             "quota": 99,
             "event_date": "2024-12-12",
             "event_time_start": "08:00",
             "event_time_end": "15:00",
             "event_longitude": "123123123",
             "event_latitude": "234234234",
             "event_image_url": "https://picsum.photos/100/200",
        }

        datax.append(event_loc)

    print(datax)

    resp_json = {
        'rc': '0000',
        'message': 'success',
        'data': datax
    }

    return json.dumps(resp_json)


if __name__ == '__main__':
    app.run()
