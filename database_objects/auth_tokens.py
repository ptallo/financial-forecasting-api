from database_objects import tools
from database_objects import table


class AuthTokenTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)

    def create_table(self):
        # Create auth token table 
        query = """CREATE TABLE auth_tokens (
                Username varchar(255) NOT NULL,
                Token varchar(255) NOT NULL,
                DateTime varchar(255) NOT NULL,
                PRIMARY KEY(Username))"""
        # Execute, commit, and close
        tools.save(query, self.db_cursor, self.db_connection)

    def remove_table(self):
        # Remove auth token table
        query = """DROP TABLE IF EXISTS auth_tokens"""
        self.db_cursor.execute(query)

    def add_token(self, username, token):
        # Add auth token to database
        query = """INSERT INTO auth_tokens (Username, Token, DateTime) VALUES ('{}', '{}', '{}')""".format(
                        username, token, tools.format_date())
        # Check query for SQL injection
        if tools.sanitize(query):
            # Insert token
            tools.save(query, self.db_cursor, self.db_connection)
            return True
        return False

    def remove_token(self, username):
        # Check username for SQL injection
        if tools.sanitize(username):
            # Remove token from database after set amount of time
            query = """DELETE FROM auth_tokens WHERE Username='{}'""".format(username)
            # Commit change to database 
            tools.save(query, self.db_cursor, self.db_connection)
            return True
        return False

    def check_token(self, username, token):
        # Select token from table to see if valid
        query = """SELECT 1 FROM auth_tokens WHERE Username='{}' AND Token='{}'""".format(username, token)
        # Sanitize
        if tools.sanitize(query):
            # Check if token is in database still
            if tools.execute(query, self.db_cursor) != []:
                # Update time stamp in token database
                update_query = """UPDATE auth_tokens SET DateTime='{}' WHERE Username='{}'""".format(tools.format_date(), username)
                # Save to database
                tools.save(update_query, self.db_cursor, self.db_connection)
                return True
            else:
                # User is not authenticated: send back to login
                return False
        else:
            # SQL injection detected: kick user out
            return False

    def cleanup_tokens(self):
        """ Function to clean up user tokens that have expired """
        # Grab current time
        cur_time = tools.format_date()
        # Grab all usernames
        results_2D = tools.select_from(["Username"], "auth_tokens", None)
        results = [result[0] for result in results_2D]
        for user in results:
            old_time = tools.select_from(["DateTime"], "auth_tokens", None)[0][0]
            # Format is YYMMDhhmmss. Expire if older than 30 minutes
            if int(cur_time) - int(old_time) >= 3000:
                self.remove_token(user)