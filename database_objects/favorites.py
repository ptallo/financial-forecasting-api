from database_objects import tools
from database_objects import table


class FavoritesTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)

    def create_fav_table(self):
        # Create user table
        query = """CREATE TABLE favorites (
                    Username varchar(255) NOT NULL,
                    Ticker varchar(10),
                    PRIMARY KEY(Username, Ticker));"""
        # Execute, commit, and close
        tools.save(query, self.db_cursor, self.db_connection, close=True)

    def remove_table(self):
        self.db_cursor.execute('DROP TABLE IF EXISTS favorites;')

    def add_favorite(self, username: str, favorite: str):
        """adds a favorite for the user, returns True if successful else False"""
        query = "SELECT 1 FROM favorites WHERE Username='{}' AND Ticker='{}'".format(
            username, favorite)
        where = "Username='{}' AND Ticker='{}'".format(username, favorite)
        # Only add favorite if no result is found
        if tools.select_from(["1"], "favorites", where, self.db_cursor) == []:
            query = "INSERT INTO favorites (Username, Ticker) VALUES ('{}', '{}')".format(
                username, favorite)
            tools.save(query, self.db_cursor, self.db_connection)
            return True
        return False

    def remove_favorite(self, username: str, favorite: str):
        """removes a favorite for the user, returns True if successful else False"""
        query = "DELETE FROM favorites WHERE Username ='{}' AND Ticker='{}';".format(
            username, favorite)
        tools.save(query, self.db_cursor, self.db_connection)
        return True

    def remove_all_favorites(self, username: str):
        query = "DELETE FROM favorites WHERE Username ='{}';".format(username)
        if tools.sanitize(query):
            tools.save(query, self.db_cursor, self.db_connection)
        return True

    def get_all_favorites(self, username: str):
        # Return all favorites of a user
        results_2D = tools.select_from(["Ticker"], "favorites", "Username='{}'".format(username))
        # Switch from 2-D array to 1-D
        results_1D = [result[0] for result in results_2D]
        return results_1D
