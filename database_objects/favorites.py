from database_objects import table


class FavoritesTable(table.DatabaseTable):
    def __init__(self, cursor=None, connection=None):
        super().__init__(cursor, connection)
        self.table_name = "favorites"

    def create_table(self):
        # Create user table
        query = """CREATE TABLE {} (
                    Username varchar(255) NOT NULL,
                    Ticker varchar(10),
                    PRIMARY KEY(Username, Ticker));""".format(self.table_name)
        # Execute, commit, and close
        self.execute(query)

    def add_favorite(self, username: str, favorite: str):
        """adds a favorite for the user, returns True if successful else False"""
        where = "Username='{}' AND Ticker='{}'".format(username, favorite)
        # Only add favorite if no result is found
        if self.select_from(["1"], where) == []:
            query = "INSERT INTO {} (Username, Ticker) VALUES ('{}', '{}')".format(
                self.table_name, username, favorite)
            self.execute(query, return_rows=False)
            return True
        return False

    def remove_favorite(self, username: str, favorite: str):
        """removes a favorite for the user, returns True if successful else False"""
        query = "DELETE FROM {} WHERE Username ='{}' AND Ticker='{}';".format(
            self.table_name, username, favorite)
        self.execute(query, return_rows=False)
        return True

    def remove_all_favorites(self, username: str):
        query = "DELETE FROM {} WHERE Username ='{}';".format(self.table_name, username)
        if self.sanitize(username):
            self.execute(query, return_rows=False)
        return True

    def get_all_favorites(self, username: str):
        # Return all favorites of a user
        results_2D = self.select_from(["Ticker"], "Username='{}'".format(username))
        # Switch from 2-D array to 1-D
        results_1D = [result[0] for result in results_2D]
        return results_1D
