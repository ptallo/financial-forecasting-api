import psycopg2 as pg2
from cred import *
from datetime import date as date
import hashlib
import time

def get_conn():
    # Establish Connection
    # TODO Remove timer
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
    # Build Query
    query = "INSERT INTO users (Username, Passwd_Hash, Email, last_login) VALUES ('{}', '{}', '{}', '{}');".format(user_name, pword_hash, email, last_login)
    # Execute and commit Query
    save(query, cur, conn)

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


def encode(password):
    # Encode user password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    pword_hash = m.hexdigest()

def save(query, cur, conn):
    # Execute query, commit, and close connection
    cur.execute(query)
    conn.commit()
    cur.close()

def execute(query, cur):
    # Execute query, return rows, and close connection
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

def tester():
    create_table()
    insert_users("krauskmr", "my_password", "krauskmr@mail.uc.edu")
    select_from(["last_login"], "users", None)

tester()