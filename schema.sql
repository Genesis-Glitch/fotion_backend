DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS registration;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  contact_number TEXT
);

CREATE TABLE event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  location_id INTEGER NOT NULL,
  event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_time_start TEXT,
  event_time_end TEXT,
  event_longitude TEXT,
  event_latitude TEXT,
  event_image_url TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (location_id) REFERENCES location(id)
);

CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    longitude TEXT NOT NULL,
    latitude TEXT NOT NULL,
    max_quota INTEGER NOT NULL,
    availability BIT
);

CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    schedule_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    schedule_quota INTEGER NOT NULL
);

CREATE TABLE food (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    name TEXT NOT NULL,
    amount FLOAT,
    unit TEXT,
    expiry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specification TEXT
);

CREATE TABLE registration (
    id INTEGER PRIMARY KEY  AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status bit,
    registration_date TIMESTAMP DEFAULT  CURRENT_TIMESTAMP
);