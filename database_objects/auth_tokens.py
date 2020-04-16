from database_objects import table

from datetime import datetime as dt, timedelta


class AuthTokenTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)
        self.table_name = "auth_tokens"
        self.format = "%m-%d-%Y-%H-%M-%S"

    def create_table(self):
        # Create auth token table
        query = """CREATE TABLE {} (
                Username varchar(255) NOT NULL,
                Token varchar(255) NOT NULL,
                DateTime varchar(255) NOT NULL,
                PRIMARY KEY(Username))""".format(self.table_name)
        # Execute and commit
        self.execute(query)

    def insert_token(self, username, token):
        # Check query for SQL injection and insert
        query = "INSERT INTO {0} (Username, Token, DateTime) VALUES ('{1}', '{2}', '{3}') ON CONFLICT (UserName) DO UPDATE SET token = '{2}', DateTime = '{3}'".format(
            self.table_name, username, token, self.dto_to_str(dt.now()))

        if self.sanitize(query):
            self.execute(query)

        inserted_token = self.get_row_for_username(username)
        if inserted_token:
            return inserted_token == token
        return False

    def dto_to_str(self, dto):
        return dto.strftime(self.format)

    def str_to_dto(self, dto_str):
        return dt.strptime(dto_str, self.format)

    def get_row_for_username(self, username):
        query = "SELECT * FROM {} WHERE Username='{}'".format(username)
        rows = self.execute_and_return_rows(query)
        if len(rows) != 1:
            return 0
        username, token, timeout = rows[0]
        return username, token,

    def get_row_for_token(self, token):
        query = "SELECT * FROM {} WHERE Token='{}'".format(token)
        rows = self.execute_and_return_rows(query)
        if len(rows) != 1:
            return 0
        username, token, timeout = rows[0]
        return username, token, self.str_to_dto(timeout)

    def is_token_timedout(self, token, timeout=1800):
        query = "SELECT * FROM {} WHERE Token='{}'".format(token)
        rows = self.execute_and_return_rows(query)
        username, token, init_time = rows[0]
        init_time = self.str_to_dto(init_time)
        return init_time + timedelta(seconds=timeout) > dt.now()

    def get_all_tokens(self):
        query = "SELECT * FROM {}"
        tokens = self.execute_and_return_rows(query)
        return [t[1] for t in tokens]
