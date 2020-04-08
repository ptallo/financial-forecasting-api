import random
import string
import hashlib
from database_objects import table
from database_objects import favorites


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
        # Execute, commit, and close
        self.save(query)

    def insert_user(self, username: str, password: str):
        """Attempts to insert a user. Return a True if the user is successfully inserted"""
        where = "Username='{}'".format(username)
        if self.select_from(["1"], where) != []:
            return False
        else:
            salt = self.create_salt()
            password_hash = self.encode(password+salt)
            query = "INSERT INTO {} (Username, Passwd_Hash, Passwd_Salt) VALUES ('{}', '{}', '{}');".format(
                self.table_name, username, password_hash, salt)
            self.save(query)
            return True

    def delete_user(self, username: str, password: str, favorites_dbo: favorites.FavoritesTable):
        if not self.authenticate_user(username, password):
            return False
        query = "DELETE FROM {} WHERE Username='{}';".format(self.table_name, username)
        self.save(query)
        favorites_dbo.remove_all_favorites(username)
        return True

    def authenticate_user(self, username: str, password: str):
        """Attempts to authenticate the user, returns True if the username and password are valid"""
        password_hash, salt = self.get_user_info(username)
        submitted_password_hash = self.encode(password+salt)
        return password_hash == submitted_password_hash

    def change_user_password(self, username: str, old_password: str, new_password: str):
        if not self.authenticate_user(username, old_password):
            return False
        new_salt = self.create_salt()
        new_password_hash = self.encode(new_password+new_salt)
        query = "UPDATE {} SET Passwd_Hash ='{}', Passwd_Salt = '{}' WHERE Username='{}';".format(
            self.table_name, new_password_hash, new_salt, username)
        self.save(query)
        return True

    def get_all_users(self):
        results2D = self.select_from(["Username"])
        results = [result[0] for result in results2D]
        return results

    def get_user_info(self, username: str):
        """get_user_info(username) -> (password_hash, salt)"""
        where = "Username='{}'".format(username)
        returned_users = self.select_from(["*"], where)[0]
        if len(returned_users) > 0:
            password_hash, salt = returned_users[1:]
        return password_hash, salt

    def create_salt(self):
        # Generate random salt consisting of letters and numbers
        salt = "".join(random.choice(string.ascii_letters+string.digits)
                    for _ in range(16))
        return salt

    def encode(self, password: str):
        # Encode user password
        m = hashlib.sha256()
        m.update(bytes(password, 'utf8'))
        return m.hexdigest()