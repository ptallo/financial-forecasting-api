import hashlib
import database_functions as df


class User(object):

    def __init__(self, user_name, password):
        self.user_name = user_name
        m = hashlib.sha256()
        m.update(bytes(password, 'utf8'))
        self.password = m.hexdigest()

    @property
    def is_active(self):
        return df.auth_user(self.user_name, self.password)

    @property
    def is_authenticated(self):
        return df.auth_user(self.user_name, self.password)

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.user_name
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
