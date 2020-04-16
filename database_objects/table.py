from database_objects import tools


class DatabaseTable:
    def __init__(self, cursor=None, connection=None):
        if cursor is None or connection is None:
            self.cur, self.conn = tools.get_conn()
        else:
            self.cur = cursor
            self.conn = connection

    def create_table(self):
        raise NotImplementedError()

    def remove_table(self):
        self.execute('DROP TABLE IF EXISTS {};'.format(self.table_name))

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
            results = self.execute_and_return_rows(query)
            # Change output to array format
            formatted_results = []
            for entry in results:
                formatted_results.append([item for item in entry if item != ''])
            return formatted_results
        else:
            return None

    @staticmethod
    def sanitize(query: str):
        """ Returns False if query is dangerous """
        # Check for sql injection
        l_query = query.lower().split()
        banned_words = ["drop", "delete", ";"]
        for word in l_query:
            if word in banned_words:
                print("Invalid input. Detected dangerous word")
                return False
        return True

    def execute(self, query: str):
        self.cur.execute(query)

    def execute_and_return_rows(self, query: str):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def close(self):
        # Close connections to database
        self.cur.close()