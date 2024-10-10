from uuid import uuid4
import qrcode
from flask import Flask, current_app, request
from flask import Flask, render_template, redirect
import json
import agent_integration
import pandas as pd

from db import get_db

from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

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

    #Location data
    db.execute("INSERT INTO location (id, name, address, longitude, latitude, max_quota, availability) VALUES(1, 'Auckland', 'Auckland', '123', '321',100, 1);")
    db.execute("INSERT INTO location (id, name, address, longitude, latitude, max_quota, availability) VALUES(2, 'Canterbury', 'Canterbury', '123', '321',100, 1);")
    db.execute("INSERT INTO location (id, name, address, longitude, latitude, max_quota, availability) VALUES(3, 'Ponsonby', 'Pnsonby', '123', '321',100, 1);")
    db.commit()

    db.close()

    return "Finished"

@app.route('/')
def homepage():  # put application's code here
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fotion - Fighting Hunger, One Meal at a Time</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #ff6f61;
            color: white;
            padding: 1em 0;
            text-align: center;
        }
        section {
            padding: 2em;
            text-align: center;
        }
        .cta {
            background-color: #ff6f61;
            color: white;
            padding: 1em;
            margin: 2em 0;
            display: inline-block;
            text-decoration: none;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 1em 0;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to Fotion</h1>
        <p>Fighting Hunger, One Meal at a Time</p>
    </header>
    <section>
        <h2>How It Works</h2>
        <p>1. <strong>Collect</strong>: We gather surplus food from restaurants, grocery stores, and events.</p>
        <p>2. <strong>Distribute</strong>: Our volunteers deliver the food to local shelters and food banks.</p>
        <p>3. <strong>Support</strong>: We provide resources and support to ensure the food reaches those who need it most.</p>
    </section>
    <section>
        <h2>Get Involved</h2>
        <p><a href="#" class="cta">Donate Food</a></p>
        <p><a href="#" class="cta">Volunteer</a></p>
        <p><a href="#" class="cta">Spread the Word</a></p>
    </section>
    <section>
        <h2>Our Impact</h2>
        <p><strong>10,000+ Meals Delivered</strong>: Thanks to our generous donors and hardworking volunteers.</p>
        <p><strong>50+ Partner Organizations</strong>: Collaborating with local shelters, food banks, and community centers.</p>
        <p><strong>Countless Smiles</strong>: Bringing hope and nourishment to those in need.</p>
    </section>
    <section>
        <h2>Testimonials</h2>
        <blockquote>"Fotion has been a lifesaver for our shelter. The food donations have made a huge difference in the lives of our residents." - Local Shelter Manager</blockquote>
        <blockquote>"Volunteering with Fotion has been an incredibly rewarding experience. It's amazing to see the direct impact of our efforts." - Fotion Volunteer</blockquote>
    </section>
    <footer>
        <p>Contact Us: info@fotion.org | (123) 456-7890 | 123 Food Drive, Auckland, New Zealand</p>
        <p>Follow Us: <a href="#" style="color: white;">Facebook</a> | <a href="#" style="color: white;">Twitter</a> | <a href="#" style="color: white;">Instagram</a></p>
    </footer>
</body>
</html>
    """

@app.route('/location')
def location():
    conn = get_db()
    event = conn.execute("SELECT * FROM location").fetchall()

    data = []
    for row in event:
        data.append(row['name'])

    conn.close()

    return json.dumps(data)

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
        "sessionId": "MYFOODSESSION",
        "question": "give me the appropriate food donation drive event dates and number of registrants available and location in json format, dont include any texts, just the json data"
    }
    response = agent_integration.lambda_handler(event, None)
    try:
        # Parse the JSON string
        if response and 'body' in response and response['body']:
            response_data = json.loads(response['body'])
            print("TRACE & RESPONSE DATA ->  ", response_data)
        else:
            print("Invalid or empty response received")
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        response_data = None 
    
    try:
        # Extract the response and trace data
        the_response = response_data['trace_data']
    except:
        the_response = "Apologies, but an error occurred. Please rerun the application" 


    # Use trace_data and formatted_response as needed
    print(f"Response Data : ", the_response)

    return the_response

# Function to parse and format response
def format_response(response_body):
    try:
        # Try to load the response as JSON
        data = json.loads(response_body)
        # If it's a list, convert it to a DataFrame for better visualization
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            return response_body
    except json.JSONDecodeError:
        # If response is not JSON, return as is
        return response_body

@app.route("/register-event/<user_id>/<event_id>", methods = ['POST', 'GET'])
def register_event(user_id, event_id):
    conn = get_db()

    conn.execute("INSERT INTO registration (user_id, event_id, status, registration_date) VALUES("+str(user_id)+","+str(event_id)+", '0', CURRENT_TIMESTAMP);")
    conn.commit()
    conn.close()

    return redirect("http://52.11.213.134/static/img_qr.png")


@app.route("/qr")
def get_qr():

    data = "http://52.11.213.134"
    img = qrcode.make(data)
    img.save('img_qr.png')

    return redirect("http://52.11.213.134/static/img_qr.png")

@app.route('/events', methods = ['GET'])
def get_events():
    conn = get_db()
    region = conn.execute("SELECT distinct name,id FROM location ORDER BY id ASC").fetchall()

    datax = []

    for r in region:
        events = conn.execute('SELECT id, title, event_image_url FROM event WHERE location_id = '+str(r['id'])).fetchall()
        print('SELECT id, title, event_image_url FROM event WHERE location_id = '+str(r['id']))
        results = [tuple(row) for row in events]

        event_data = []
        for row in events:
            event_loc = {"id":str(row[0]),"title":row[1],"url": row[2]}

            event_data.append(event_loc)

        print(event_data)

        region = {
            'title': r['name'],
            'images': event_data,
        }

        datax.append(region)

    print(datax)

    resp_json = datax

    conn.close()
    return json.dumps(resp_json)


if __name__ == '__main__':
    app.run()
