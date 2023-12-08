import sqlite3
from flask import g
from datetime import datetime
import os
import base64
from sqlite3 import IntegrityError
DATABASE = 'site.db'
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with open(DB_PATH, 'r') as f:
        get_db().cursor().executescript(f.read())
    get_db().commit()

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    #print(rv[0])
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv
def generate_base64_string():
    random_bytes = os.urandom(16)
    base64_string = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
    return base64_string

def signup_db(username, email, password):
    try:
        new_user_id = generate_base64_string()
        new_user_token = generate_base64_string()

    
        password_hash = password
        query = '''
        INSERT INTO user (id, username, email, password_hash, user_token, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        args = (new_user_id, username, email, password_hash, new_user_token, datetime.utcnow())

        cur = get_db().execute(query, args)
        get_db().commit()
        cur.close()

        return new_user_id
    except IntegrityError:
        
        return 

def insert_problem(title, thumbnail, link, description):
    query = '''
    INSERT INTO problems (title, thumbnail, link, description)
    VALUES (?, ?, ?, ?)
    '''
    args = (title, thumbnail, link, description)

    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()
def drop_problems_table():
    db = get_db()
    
    cur = db.cursor()
    cur.execute('DROP TABLE IF EXISTS problems')
    db.commit()

def get_problem():
    db = get_db()
    cur = db.execute('SELECT * FROM problems')
    titles = [row for row in cur.fetchall()]
    return titles
def get_solution():
    db = get_db()
    cur = db.execute('SELECT * FROM solutions')
    sol = [row for row in cur.fetchall()]
    print(sol)
    return sol

def save_solution_to_db(problem_id, user_id, solution_description, language, github_link):
    try:
        # Connect to the database
        db = get_db()

        # Use an INSERT statement to save the solution to the solutions table
        query = 'INSERT INTO solutions (problem_id, user_id, solution_description, language, github_link) VALUES (?, ?, ?, ?, ?)'
        db.execute(query, (problem_id, user_id, solution_description, language, github_link))
        db.commit()

        # Optionally, you can fetch the inserted solution ID or perform other operations

    except sqlite3.Error as e:
        # Handle the error (e.g., log it, display a message)
        print(f"Error saving solution to the database: {e}")

def get_user_by_id(user_id):
    db = get_db()
    # cur = db.execute(f'SELECT * FROM user WHERE user_token = {user_id}')
    # user = cur.fetchone()
    return 
