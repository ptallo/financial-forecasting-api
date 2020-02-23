import psycopg2 as pg2
from cred import *
from datetime import date as date
import hashlib
import time

def get_conn():
    # Establish Connection
    # TODO Remove timer
    if DEBUG:
        tic = time.perf_counter()
    # Try to connect
    try:
        query = "dbname='{}' user='{}' host='{}' password='{}'".format(
                dbase_name, user, host, password)
        conn = pg2.connect(query)
    # TODO Handle connection failure
    except:
        print("Error! Failed to connect")

    # Establish cursor
    cur = conn.cursor()
    # TODO Remove debug code
    if DEBUG:
        toc = time.perf_counter()
        print(f"Established connection in {toc - tic:0.4f} seconds")
    return cur, conn


def create_table():
    # Establish connection
    cur, conn = get_conn()
    # TODO Remove later
    cur.execute('DROP TABLE IF EXISTS users;')
    # Create user table
    query = """CREATE TABLE users (
                            Username varchar(255) NOT NULL,
                            Passwd_Hash varchar(255) NOT NULL,
                            Email varchar(255) NOT NULL,
                            last_login DATE NOT NULL,
                            PRIMARY KEY (Username, Email));"""
    # Execute, commit, and close
    save(query, cur, conn)

def insert_users(user_name, pword, email):
    # Insert into table Users
    cur, conn = get_conn()
    # Grab current date
    last_login = date.today()
    # Hash password
    pword_hash = encode(pword)
    # Query to see if username taken
    query_user = "SELECT 1 FROM users WHERE Username='{}' ;".format(user_name)
    # Query to see if email is in use
    query_email = "SELECT 1 FROM users WHERE Email='{}';".format(email)
    # Exit if username taken
    if execute(query_email, cur):
        print("The email "+ email + " is already associated with an account!")
        cur.close()
        return
    # Exit if email is in use
    elif execute(query_user, cur):
        print("The username " + user_name + " is already in use!")
        cur.close()
        return
    else:
        # Build Query
        query = "INSERT INTO users (Username, Passwd_Hash, Email, last_login) VALUES ('{}', '{}', '{}', '{}');".format(user_name, pword_hash, email, last_login)
        # Execute and commit query
        save(query, cur, conn)

def auth_user(user_name, pword):
    # Get connection
    cur, conn = get_conn()
    # Hash password
    pword_hash = encode(pword)
    # Returns object if match; [] if no match
    query = "SELECT 1 FROM users WHERE Username='{}' and Passwd_Hash='{}';".format(user_name, pword_hash)
    return execute(query, cur, close=True) != []

def change_password(user_name, old_pass, new_pass):
    # Ensure old password matches
    if not auth_user(user_name, old_pass):
        print('Old password incorrect')
        return
    # Get connection
    cur, conn = get_conn()
    pword_hash = encode(new_pass)
    query = "UPDATE users SET Passwd_Hash ='{}' WHERE Username='{}';".format(pword_hash, user_name)
    save(query, cur, conn)
    print("Update successful")

def delete_from():
    cur, conn = get_conn()
    cur.close()
    pass

def select_from(fields, table, conditions):
    # Get connection 
    cur, conn = get_conn()
    # Build fields string to select
    field_str = " "
    for field in fields[:-1]:
        field_str += field + ", "
    field_str += fields[-1]

    # Build query
    query = 'SELECT {} FROM {}'.format(field_str, table)
    # Handle special conditions
    if conditions:
        query += ' WHERE ' + conditions
    query += ";"

    # Execute query
    rows = execute(query, cur)
    for row in rows:
        print(row)
    cur.close()

# TODO modify for final product
def encode(password):
    # Encode user password
    if not DEBUG:
        return password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    return m.hexdigest()

def save(query, cur, conn):
    # Execute query, commit, and close connection
    cur.execute(query)
    conn.commit()
    cur.close()

def execute(query, cur, close=False):
    # Execute query, return rows, and close connection
    cur.execute(query)
    rows = cur.fetchall()
    if close:
        cur.close()
    return rows


def tester():
    #create_table()
    #insert_users("krauskmr", "my_password", "krauskmr@mail.uc.edu")
    #select_from(["*"], "users", None)
    #print(auth_user("krauskmr", "my_password"))
    change_password("krauskmr","new_password","old_password")

if __name__ == '__main__':
    DEBUG = 1
    tester()