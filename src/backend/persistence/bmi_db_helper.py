import sqlite3

DB_NAME = "data/bmi_database.db"

#get connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn

#initialize db
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    filepath = "src/backend/persistence/bmi_user_schema.sql"
    with open(filepath, 'r') as f:
        cursor.executescript(f.read())

    conn.close()

def insert_user(record):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Insert state (if not exists)
    cur.execute("""
        INSERT OR IGNORE INTO states (state_name)
        VALUES (?)
    """, (record["state"],))

    cur.execute("""
        SELECT state_id FROM states WHERE state_name = ?
    """, (record["state"],))
    state_id = cur.fetchone()[0]

    # 2. Insert city (if not exists)
    cur.execute("""
        INSERT OR IGNORE INTO cities (city_name, state_id)
        VALUES (?, ?)
    """, (record["city"], state_id))

    cur.execute("""
        SELECT city_id FROM cities WHERE city_name = ?
    """, (record["city"],))
    city_id = cur.fetchone()[0]

    # 3. Insert person
    cur.execute("""
        INSERT INTO persons (
            name, email, age, height_cm, weight_kg,
            bmi, bmi_category, city_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["name"],
        record["email"],
        record["age"],
        record["height_cm"],
        record["weight_kg"],
        record["bmi"],
        record["bmi_category"],
        city_id
    ))

    conn.commit()
    person_id = cur.lastrowid
    conn.close()

    return person_id

# fetch/read user
def fetch_all():
    conn = get_connection()
    cur = conn.cursor()
   
    rows = conn.execute("SELECT * FROM persons").fetchall()   
    result  = []

    for row in rows:
        row_dict = dict(row)
        city_data = conn.execute("SELECT * FROM cities WHERE city_id = ?", (row_dict["city_id"],)).fetchone()
        state_data = conn.execute("SELECT * FROM states WHERE state_id = ?", (city_data["state_id"],)).fetchone()
        row_dict["city"] = city_data["city_name"]
        row_dict["state"] = state_data["state_name"]

        # update rows_dict in rows with city and state names
        result.append(row_dict)
   
    conn.close()
    return result

 # get one user   
def fetch_by_id(record_id):
    conn= get_connection()
    row = conn.execute("SELECT * FROM persons WHERE persons_id = ?", (record_id,)).fetchone()
    conn.close()

    return dict(row) if row else None

# update user

# delete user
def delete_record(record_id):
    conn = get_connection()
   
    conn.execute("DELETE FROM persons WHERE persons_id = ?", (record_id,))

    conn.commit()
    conn.close()

# additional db operations for bmi per city and state modules

# def add_person_to_db(person, city_id):
#     conn = get_connection()

#     cur = conn.cursor()
#     cur.execute("INSERT OR IGNORE INTO persons (name, gender, age, height_cm, weight_kg, bmi, bmi_category, city_id) VALUES(?,?,?,?,?,?,?,?)",
#                 (person["name"], person["gender"], person["age"], person["height_cm"], person["weight_kg"], person["bmi"], person["bmi_category"], city_id))
    
#     conn.commit()
#     conn.close()


# def insert_city(city, state_id): # TODO: remove?
#     conn = get_connection()

#     cur = conn.cursor()
#     cur.execute("INSERT OR IGNORE INTO cities (city_name, state_id) VALUES(?,?)", (city, state_id))
    
#     conn.commit()
#     conn.close()    

# def insert_state(state): # TODO: remove?
#     conn = get_connection()

#     cur = conn.cursor()
#     cur.execute("INSERT OR IGNORE INTO states (state_name) VALUES (?)", [state])
       
#     conn.commit()
#     conn.close()

def get_state_id(state):
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT state_id FROM states where state_name=(?)", [state])
    ret = cur.fetchone()
    
    conn.commit()
    conn.close()
    return ret[0]

def get_city_id(city):
    conn = get_connection() 

    cur = conn.cursor()
    cur.execute("SELECT city_id FROM cities where city_name=(?)", [city])
    ret = cur.fetchone()

    conn.commit()
    conn.close()
    return ret[0]

def get_all_states():
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT state_name FROM states")
    
    states = []
    for s in cur.fetchall():
        states.append(s[0])
 
    conn.commit()
    conn.close()
    return states

def get_cities_id_for_state(id):
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT city_id FROM cities WHERE state_id=(?)", [id])

    city_ids = [row[0] for row in cur.fetchall()]
 
    conn.commit()
    conn.close()
    return city_ids

def get_person_data_for_city(id):
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT weight_kg, height_cm FROM persons WHERE city_id = (?)", [id])
    ret = cur.fetchone()

    conn.commit()
    conn.close()
    return ret
