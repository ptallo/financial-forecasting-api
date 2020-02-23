import psycopg2 as pg2

def get_conn():
    dbase_name = ""
    user = ""
    host = ""
    password = ""
    try:
        conn = pg2.connect("dbname='" + dbase_name + "' user='" + user +
                       "' host='" + host + "' password='" + password + "'")
    except:
        pass
        #Handle connection error
    cur = conn.cursor()
    return cur

def create_table():
    cur = get_conn()
    pass

def insert_into():
    cur = get_conn()
    pass

def delete_from():
    cur = get_conn()
    pass

def select_from(fields, table, conditions):
    cur = get_conn()
    field_str = " "
    for field in fields[:-1]:
        field_str += field + ", "
    field_str += fields[-1]

    query = '''SELECT ''' + field_str + ''' FROM ''' + table
    cur.execte(query)