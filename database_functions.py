import psycopg2 as pg2
from cred import * # Import login credentials
import hashlib

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

def create_user_table():
    # Establish connection
    cur, conn = get_conn()
    # TODO Remove later
    cur.execute('DROP TABLE IF EXISTS users;')
    # Create user table
    query = """CREATE TABLE users (
                            Username varchar(255) NOT NULL,
                            Passwd_Hash varchar(255) NOT NULL,
                            PRIMARY KEY (Username));"""
    # Execute, commit, and close
    save(query, cur, conn, close=True)

def create_fav_table():
    # Establish connection
    cur, conn = get_conn()
    # TODO Remove later
    cur.execute('DROP TABLE IF EXISTS favorites;')
    # Create user table
    query = """CREATE TABLE favorites (
                            Username varchar(255) NOT NULL,
                            Ticker varchar(10),
                            PRIMARY KEY(Username, Ticker));"""
    # Execute, commit, and close
    save(query, cur, conn, close=True)

def add_favorite(user_name, favorite):
    # Establish connection
    cur, conn = get_conn()
    # Check if favorite already exists
    query = "SELECT 1 FROM favorites WHERE Username='{}' AND Ticker='{}'".format(user_name, favorite)
    # Condition query
    where = "Username='{}' AND Ticker='{}'".format(user_name, favorite)
    # Only add favorite if no result is found
    if select_from(["1"], "favorites", where, cur) == []:
        query = "INSERT INTO favorites (Username, Ticker) VALUES ('{}', '{}')".format(user_name, favorite)
        # Save transaction
        save(query, cur, conn)
    cur.close()

def remove_favorite(user_name, favorite):
    # Establish Connection
    cur, conn = get_conn()
    # Remove favorite
    query = "DELETE FROM favorites WHERE Username ='{}' AND Ticker='{}';".format(user_name, favorite)
    # Save transaction
    save(query, cur, conn)


def insert_user(user_name, pword):
    # Insert into table Users
    cur, conn = get_conn()
    # Query to see if username taken
    query_user = "SELECT 1 FROM users WHERE Username='{}' ;".format(user_name)
    # Exit if username taken
    if execute(query_user, cur):
        print("The username " + user_name + " is already in use!")
        cur.close()
        return (400, error)
    else:
        # Hash password
        pword_hash = encode(pword)
        # Build Query
        query = "INSERT INTO users (Username, Passwd_Hash) VALUES ('{}', '{}');".format(user_name, pword_hash)
        # Execute and commit query
        save(query, cur, conn, close=True)
        return (201, "User succesfully inserted")

def delete_user(user_name, pword):
    # Ensure user account exists before deleting
    if not auth_user(user_name, pword):
        print('Error: Cannot delete account')
        return
    # Get connection
    cur, conn = get_conn()
    pword_hash = encode(pword)
    # TODO Delete other tables after created
    # Delete user from users tables
    query = "DELETE FROM users WHERE Passwd_Hash ='{}' AND Username='{}';".format(pword_hash, user_name)
    # Commit database deletion
    save(query, cur, conn)
    # Delete user favorites
    query = "DELETE FROM favorites WHERE Username ='{}';".format(user_name)
    save(query, cur, conn, close=True)
    print("User account deleted")

def auth_user(user_name, pword):
    # Get connection
    cur, conn = get_conn()
    # Hash password
    pword_hash = encode(pword)
    # Returns object if match; [] if no match
    query = "SELECT 1 FROM users WHERE Username='{}' and Passwd_Hash='{}';".format(user_name, pword_hash)
    # Return True if user found, False if no match
    return execute(query, cur, close=True) != []

def change_password(user_name, old_pass, new_pass):
    # Ensure old password matches
    if not auth_user(user_name, old_pass):
        print('Old password incorrect')
        return
    # Get connection
    cur, conn = get_conn()
    # Encode password
    pword_hash = encode(new_pass)
    # Update password hash in database
    query = "UPDATE users SET Passwd_Hash ='{}' WHERE Username='{}';".format(pword_hash, user_name)
    save(query, cur, conn, close=True)
    print("Update successful")

def select_from(fields, table, conditions, cur=None):
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
    print(query)

    # Execute query
    return execute(query, cur)

def sanitize(query):
    l_query = query.lower()
    banned_words = ["drop", "delete", ";"]
    for word in banned_words:
        if word in query:
            print("Invalid input. Detected dangerous word")
            return False
    return True

def encode(password):
    # Encode user password
    m = hashlib.sha256()
    m.update(bytes(password, 'utf8'))
    return m.hexdigest()

def save(query, cur, conn, close=False):
    # Execute query, commit, and close connection
    cur.execute(query)
    conn.commit()
    if close:
        cur.close()

def execute(query, cur, close=False):
    # Execute query, return rows, and close connection
    cur.execute(query)
    rows = cur.fetchall()
    if close:
        cur.close()
    return rows

def tester():
    #create_user_table()
    #create_fav_table()
    #change_password("krauskmr","new_password","old_password")
    #insert_user("krauskmr", "my_password")
    #print(select_from(["*"], "users", None))
    #delete_user("krauskmr", "my_password")
    #add_favorite("krauskmr", "dfs")
    #remove_favorite("krauskmr", "dfs")
    #add_favorite("krauskmr", "ABC")
    #print(select_from(["*"], "favorites", None))
    pass


if __name__ == '__main__':
    tester()