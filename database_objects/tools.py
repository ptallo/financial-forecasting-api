import psycopg2 as pg2
from cred import *  # Import login credentials
import hashlib
import random
import string


def get_conn():
    # Establish Connection
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
    return cur, conn


def select_from(fields: list, table: str, conditions: str, cur=None):
    if cur == None:
        cur, _ = get_conn()
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
    # Add ending ;
    query += ";"

    # Execute query
    return execute(query, cur)


def sanitize(query: str):
    l_query = query.lower()
    banned_words = ["drop", "delete", ";"]
    for word in banned_words:
        if word in query:
            print("Invalid input. Detected dangerous word")
            return False
    return True


def encode(password: str):
    # Encode user password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    return m.hexdigest()


def create_salt():
    # Generate random salt consisting of letters and numbers
    salt = "".join(random.choice(string.ascii_letters+string.digits)
                   for _ in range(16))
    return salt


def save(query: str, cur, conn, close=False):
    # Execute query, commit, and close connection
    cur.execute(query)
    conn.commit()
    if close:
        cur.close()


def execute(query: str, cur, close=False):
    # Execute query, return rows, and close connection
    cur.execute(query)
    rows = cur.fetchall()
    if close:
        cur.close()
    return rows
