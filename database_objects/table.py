from database_objects import tools
import psycopg2 as pg2
from cred import * # Import login credentials


class DatabaseTable:
    def __init__(self, cursor=None, connection=None):
        if cursor is None or connection is None:
            self.get_conn()
        else:
            self.cur = cursor
            self.conn = connection

    def create_table(self):
        raise NotImplementedError()

    def remove_table(self):
        self.cur.execute('DROP TABLE IF EXISTS {};'.format(self.table_name))

    def select_from(self, fields: list, conditions: str = None):
        ''' Returns 2-D array of query results '''
        # Build fields string to select
        field_str = " "
        for field in fields[:-1]:
            field_str += field + ", "
        field_str += fields[-1]

        # Build query
        query = 'SELECT {} FROM {}'.format(field_str, self.table_name)
        # Handle special conditions
        if conditions:
            query += ' WHERE ' + conditions

        # Execute query
        if self.sanitize(query):
            results = self.execute(query)
            # Change output to array format
            formatted_results = []
            for entry in results:
                formatted_results.append([item for item in entry if item != ''])
            return formatted_results
        else:
            return None


    def sanitize(self, query: str):
        # Check for sql injection
        l_query = query.lower().split()
        banned_words = ["drop", "delete", ";"]
        for word in l_query:
            if word in banned_words:
                print("Invalid input. Detected dangerous word")
                return False
        return True

    def get_conn(self):
        # Establish Connection
        # Try to connect
        try:
            query = "dbname='{}' user='{}' host='{}' password='{}'".format(
                    dbase_name, user, host, password)
            self.conn = pg2.connect(query)
        # TODO Handle connection failure
        except:
            print("Error! Failed to connect")

        # Establish cursor
        self.cur = self.conn.cursor()

    def execute(self, query: str):
        # Execute query and return rows
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def close(self):
        # Close connections to database
        self.cur.close()

    def save(self, query: str):
        # Execute query and save result
        self.cur.execute(query)
        self.conn.commit()