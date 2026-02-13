/*

Module to set up the SQLite database and create necessary tables for BMI data storage.

*/
CREATE TABLE IF NOT EXISTS states(
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_name TEXT UNIQUE   
    );

CREATE TABLE IF NOT EXISTS cities(
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT UNIQUE, 
    state_id INTEGER,
    FOREIGN KEY(state_id) REFERENCES states(state_id)
    );

CREATE TABLE IF NOT EXISTS persons ( 
    persons_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    height_cm REAL NOT NULL,
    weight_kg REAL NOT NULL,
    bmi REAL NOT NULL,
    bmi_category TEXT NOT NULL,
    city_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
    );
