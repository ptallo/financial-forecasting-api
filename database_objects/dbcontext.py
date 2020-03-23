from database_objects import tools
from database_objects import users
from database_objects import favorites


class DatabaseContext:
    def __init__(self):
        self.db_cursor, self.db_connection = tools.get_conn()
        self.users = users.UsersTable(self.db_cursor, self.db_connection)
        self.favorites = favorites.FavoritesTable(
            self.db_cursor, self.db_connection)

    def close_context(self):
        self.db_cursor.close()
