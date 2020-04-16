import random
import string
from database_objects import table
from database_objects import favorites
from database_objects import tools


class UsersTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)
        self.table_name = "users"

    def create_table(self):
        # Create user table
        query = """CREATE TABLE {} (
                Username varchar(255) NOT NULL,
                Passwd_Hash varchar(255) NOT NULL,
                Passwd_Salt varchar(16) NOT NULL,
                PRIMARY KEY (Username));""".format(self.table_name)
        # Execute and commit
        self.execute(query)

    def insert_user(self, username: str, password: str):
        """Attempts to insert a user. Return a True if the user is successfully inserted"""
        if not self.sanitize(username):  # check for properly sanitized username
            raise Exception("Username not sanitized properly!")
        elif self.get_user_info(username):  # check if user already exists
            return False

        # insert user
        salt = self.create_salt()
        password_hash = self.get_pass_hash(password, salt)
        query = "INSERT INTO {} (Username, Passwd_Hash, Passwd_Salt) VALUES ('{}', '{}', '{}');".format(
            self.table_name, username, password_hash, salt)
        self.execute(query)

        # check if user was inserted successfully
        return True if self.get_user_info(username) else False

    def delete_user(self, username: str, favorites_dbo: favorites.FavoritesTable):
        # check if user exists, if not return False
        if not self.get_user_info(username):
            return False

        # delete user
        query = "DELETE FROM {} WHERE Username='{}';".format(
            self.table_name, username)
        self.execute(query)

        # check if the user was successfully deleted
        return True if not self.get_user_info(username) and favorites_dbo.remove_all_favorites(username) else False

    def change_user_password(self, username: str, old_password: str, new_password: str):
        if not self.get_user_info(username):  # check if user exists
            return False
        # check if user knows password
        if not self.authenticate_user(username, old_password):
            return False

        # Update pass info for user
        new_salt = self.create_salt()
        new_password_hash = self.get_pass_hash(new_password, new_salt)
        query = "UPDATE {} SET Passwd_Hash ='{}', Passwd_Salt = '{}' WHERE Username='{}';".format(
            self.table_name, new_password_hash, new_salt, username)
        self.execute(query)

        # Check user pass info is now correct
        username, pass_hash, salt = self.get_user_info(username)
        return self.get_pass_hash(new_password, salt) == new_password_hash

    def authenticate_user(self, username: str, password: str):
        """Attempts to authenticate the user, returns True if the username and password are valid"""
        if not self.get_user_info(username):
            return False
        username, password_hash, salt = self.get_user_info(username)
        submitted_password_hash = self.get_pass_hash(password, salt)
        return password_hash == submitted_password_hash

    def get_all_users(self):
        results2D = self.select_from(["Username"])
        query = "SELECT * FROM {}".format(self.table_name)
        users = self.execute_and_return_rows(query)
        results = [result[0] for result in results2D]
        return results

    def get_user_info(self, username: str):
        """get_user(username) -> (username, password_hash, salt)"""
        query = "SELECT * FROM {} WHERE Username='{}'".format(
            self.table_name, username)
        users = self.execute_and_return_rows(query)
        if len(users) != 1:
            return
        username, password_hash, salt = users[0]
        return username, password_hash, salt

    def get_pass_hash(self, password: str, salt: str):
        return tools.encode(password+salt)

    def create_salt(self):
        # Generate random salt consisting of letters and numbers
        salt = "".join(random.choice(string.ascii_letters+string.digits)
                       for _ in range(16))
        return salt
