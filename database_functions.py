import psycopg2 as pg2
from cred import *
from datetime import date as date
import hashlib

def get_conn():
    try:
        query = "dbname='{}' user='{}' host='{}' password='{}'".format(
                dbase_name, user, host, password)
        conn = pg2.connect(query)
    except:
        print("Error! Failed to connect")
        #Handle connection error
    cur = conn.cursor()
    return cur, conn

def close_conn(cur):
    cur.close()

def create_table():
    cur, conn = get_conn()
    cur.execute('DROP TABLE IF EXISTS users;')
    query = """CREATE TABLE users (
                            Username varchar(255) NOT NULL,
                            Passwd_Hash varchar(255) NOT NULL,
                            Email varchar(255) NOT NULL,
                            last_login DATE NOT NULL,
                            PRIMARY KEY (Username, Email));"""
    if not cur.execute(query):
        print("Success!")
    else:
        print("Failure....")
    conn.commit()
    close_conn(cur)

def insert_into(user_name, pword, email):
    cur, conn = get_conn()
    last_login = date.today()
    m = hashlib.sha256()
    m.update(bytes(pword, 'utf8'))
    pword_hash = m.hexdigest()
    query = "INSERT INTO users (Username, Passwd_Hash, Email, last_login) VALUES ('{}', '{}', '{}', '{}');".format(user_name, pword_hash, email, last_login)
    cur.execute(query)
    conn.commit()
    close_conn(cur)

def delete_from():
    cur, conn = get_conn()
    close_conn(cur)
    pass

def select_from(fields, table, conditions):
    cur, conn = get_conn()
    field_str = " "
    for field in fields[:-1]:
        field_str += field + ", "
    field_str += fields[-1]

    query = 'SELECT {} FROM {}'.format(field_str, table)
    if conditions:
        query += ' WHERE ' + conditions
    query += ";"

    cur.execute(query)

    rows = cur.fetchall()
    for row in rows:
        print(row)
    close_conn(cur)

def tester():
    create_table()
    insert_into("krauskmr", "my_password", "krauskmr@mail.uc.edu")
    select_from(["last_login"], "users", None)

tester()