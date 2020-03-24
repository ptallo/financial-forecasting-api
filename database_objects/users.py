from database_objects import tools
from database_objects import table
from database_objects import favorites


class UsersTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)

    def create_table(self):
        # Create user table
        query = """CREATE TABLE users (
                Username varchar(255) NOT NULL,
                Passwd_Hash varchar(255) NOT NULL,
                Passwd_Salt varchar(16) NOT NULL,
                PRIMARY KEY (Username));"""
        # Execute, commit, and close
        tools.save(query, self.db_cursor, self.db_connection)

    def remove_table(self):
        self.db_cursor.execute('DROP TABLE IF EXISTS users;')

    def insert_user(self, username: str, password: str):
        """Attempts to insert a user, while return a True if the user is successfully inserted"""
        if tools.execute("SELECT 1 FROM users WHERE Username='{}' ;".format(username), self.db_cursor):
            return False
        else:
            salt = tools.create_salt()
            password_hash = tools.encode(password+salt)
            query = "INSERT INTO users (Username, Passwd_Hash, Passwd_Salt) VALUES ('{}', '{}', '{}');".format(
                username, password_hash, salt)
            tools.save(query, self.db_cursor, self.db_connection)
            return True

    def delete_user(self, username: str, password: str, favorites_dbo: favorites.FavoritesTable):
        if not self.authenticate_user(username, password):
            return False
        query = "DELETE FROM users WHERE Username='{}';".format(username)
        tools.save(query, self.db_cursor, self.db_connection)
        favorites_dbo.remove_all_favorites(username)
        return True

    def authenticate_user(self, username: str, password: str):
        """Attempts to authenticate the user, returns True if the username and password are valid"""
        password_hash, salt = self.get_user_info(username)
        submitted_password_hash = tools.encode(password+salt)
        return password_hash == submitted_password_hash

    def change_user_password(self, username: str, old_password: str, new_password: str):
        if not self.authenticate_user(username, old_password):
            return False
        new_salt = tools.create_salt()
        new_password_hash = tools.encode(new_password+new_salt)
        query = "UPDATE users SET Passwd_Hash ='{}', Passwd_Salt = '{}' WHERE Username='{}';".format(
            new_password_hash, new_salt, username)
        tools.save(query, self.db_cursor, self.db_connection)
        return True

    def get_all_users(self):
        return tools.execute("SELECT * FROM users", self.db_cursor)

    def get_user_info(self, username: str):
        """get_user_info(username) -> (password_hash, salt)"""
        returned_users = tools.execute("SELECT * FROM users WHERE Username='{}'".format(username), self.db_cursor)
        if len(returned_users) > 0:
            username, password_hash, salt = returned_users[0]
        return password_hash, salt
