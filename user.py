from database_functions import insert_user, delete_user, auth_user, change_password
from flask_login import UserMixin

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        return self.is_authenticated()

    def is_authenticated(self):
        return auth_user(self.username, self.password)

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.username.decode("utf-8")
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')