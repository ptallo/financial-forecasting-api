from database_objects import table

from datetime import datetime as dt


class AuthTokenTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)
        self.table_name = "auth_tokens"

    def create_table(self):
        # Create auth token table 
        query = """CREATE TABLE {} (
                Username varchar(255) NOT NULL,
                Token varchar(255) NOT NULL,
                DateTime varchar(255) NOT NULL,
                PRIMARY KEY(Username))""".format(self.table_name)
        # Execute, commit, and close
        self.execute(query)

    def add_token(self, username, token):
        # Add auth token to database
        query = """INSERT INTO {} (Username, Token, DateTime) VALUES ('{}', '{}', '{}') ON CONFLICT (UserName) DO UPDATE SET token = '{}', DateTime = '{}'""".format(
                        self.table_name, username, token, self.format_date(), token, self.format_date())
        # Check query for SQL injection
        if self.sanitize(query):
            # Insert token
            self.execute(query, return_rows=False)
            return True
        return False

    def get_all_tokens(self):
        query = """SELECT Username, Token FROM auth_tokens"""
        result = self.execute(query)
        return result

    def remove_token(self, username):
        # Check username for SQL injection
        if self.sanitize(username):
            # Remove token from database after set amount of time
            query = """DELETE FROM {} WHERE Username='{}'""".format(self.table_name, username)
            # Commit change to database 
            self.execute(query)
            return True
        return False

    def check_token(self, username, token):
        # Select token from table to see if valid
        where = "Username='{}' AND Token='{}'""".format(username, token)
        # Sanitize
        if self.sanitize(where):
            # Check if token is in database still
            if self.select_from(["1"], where) != []:
                # Update time stamp in token database
                update_query = """UPDATE {} SET DateTime='{}' WHERE Username='{}'""".format(self.table_name, self.format_date(), username)
                # Save to database
                self.execute(update_query)
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
        cur_time = self.format_date()
        # Grab all usernames
        results_2D = self.select_from(["Username"])
        results = [result[0] for result in results_2D]
        for user in results:
            old_time = self.select_from(["DateTime"])[0][0]
            # Format is YYMMDhhmmss. Expire if older than 30 minutes
            if int(cur_time) - int(old_time) >= 3000:
                self.remove_token(user)

    def format_date(self):
        # Grab datetime object
        today = dt.now()
        # Format MM/DD/YY into YYMMDD
        MDY = today.strftime("%x").split("/")
        YMD = MDY[2] + MDY[0] + MDY[1]
        # Grab time
        time = today.strftime("%X").replace(":", "")
        date = YMD + time
        return date