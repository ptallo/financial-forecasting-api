from database_objects import users
from database_objects import favorites
from database_objects import auth_tokens


class DatabaseContext:
    def __init__(self):
        self.users = users.UsersTable()
        self.favorites = favorites.FavoritesTable()
        self.auth_tokens = auth_tokens.AuthTokenTable()
