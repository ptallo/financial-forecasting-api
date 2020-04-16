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
        # abort if value is already in table
        if favorite in self.get_favorites(username):
            return True

        # Insert value
        query = "INSERT INTO {} (Username, Ticker) VALUES ('{}', '{}')".format(
            self.table_name, username, favorite)
        self.execute(query)
        
        # Check if value was inserted properly
        return True if favorite in self.get_favorites(username) else False

    def remove_favorite(self, username: str, favorite: str):
        """removes a favorite for the user, returns True if successful else False"""
        # check if favorite exists for user
        if favorite not in self.get_favorites(username): 
            return True

        # Delete favorite on user
        query = "DELETE FROM {} WHERE Username ='{}' AND Ticker='{}';".format(
            self.table_name, username, favorite)
        self.execute(query)

        # Check if favorite exists on user
        return True if favorite not in self.get_favorites(username) else False

    def remove_all_favorites(self, username: str):
        query = "DELETE FROM {} WHERE Username ='{}';".format(self.table_name, username)
        if self.sanitize(username):
            self.execute(query)
        return len(self.get_favorites(username)) == 0

    def get_favorites(self, username: str):
        # Return all favorites of a user
        results_2D = self.select_from(["Ticker"], "Username='{}'".format(username))
        # Switch from 2-D array to 1-D
        results_1D = [result[0] for result in results_2D]
        return results_1D
