from database_objects import tools


class DatabaseTable:
    def __init__(self, cursor=None, connection=None):
        if cursor is None or connection is None:
            self.db_cursor, self.db_connection = tools.get_conn()
        else:
            self.db_cursor = cursor
            self.db_connection = connection

    def create_table(self):
        raise NotImplementedError()

    def remove_table(self):
        raise NotImplementedError()
