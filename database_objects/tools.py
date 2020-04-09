import hashlib
import psycopg2 as pg2

from cred import dbase_name, user, host, password # Import login credentials


def encode(password: str):
    # Encode user password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    return m.hexdigest()


def get_conn():
    # Establish Connection
    # Try to connect
    try:
        query = "dbname='{}' user='{}' host='{}' password='{}'".format(
                dbase_name, user, host, password)
        conn = pg2.connect(query)
        return conn, conn.cursor()
    # TODO Handle connection failure
    except:
        print("Error! Failed to connect")
