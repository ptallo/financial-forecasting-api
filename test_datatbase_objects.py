from database_objects import users
from database_objects import favorites
from database_objects import auth_tokens


testuser_info = {
    "username": "testuser",
    "password": "chrisisdumb",
    "passwordChange": "ma22ispoopoo",
    "favorite": "AAPL",
    "favoriteTwo": "TSLA"
}


def run_all_db_tests():
    table_tests = [
        run_user_dbo_tests,
        run_favorites_dbo_tests
    ]

    total, failed = 0, 0
    for table_test in table_tests:
        t, f = table_test()
        total += t
        failed += f

    print('{} tests passed! {} tests failed!'.format(total-failed, failed))


def run_favorites_dbo_tests():
    favorites_dbo = favorites.FavoritesTable()
    user_dbo = users.UsersTable()
    favorites_dbo_tests = [
        test_add_remove_favorite,
        test_remove_all_favorites
    ]

    failed_tests = 0
    for test in favorites_dbo_tests:
        try:
            test(user_dbo, favorites_dbo)
        except AssertionError:
            failed_tests += 1

    favorites_dbo.close()
    user_dbo.close()
    return len(favorites_dbo_tests), failed_tests


def test_add_remove_favorite(user_dbo: users.UsersTable, favorites_dbo: favorites.FavoritesTable):
    if not user_dbo.insert_user(testuser_info.get("username"), testuser_info.get("passwordChange")):
        raise Exception('test not set up properly')

    assertEqual(favorites_dbo.add_favorite(testuser_info.get(
        'username'), testuser_info.get('favorite')), True)

    assertEqual(favorites_dbo.get_all_favorites(testuser_info.get(
        'username')), [testuser_info.get('favorite'), testuser_info.get('favoriteTwo')])

    assertEqual(favorites_dbo.remove_favorite(testuser_info.get(
        'username'), testuser_info.get('favorite')), True)

    if not user_dbo.delete_user(testuser_info.get("username"), testuser_info.get("passwordChange"), favorites_dbo):
        raise Exception('test not cleaned up properly')


def test_remove_all_favorites(user_dbo: users.UsersTable, favorites_dbo: favorites.FavoritesTable):
    inserted_user = user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("passwordChange"))
    inserted_fav1 = favorites_dbo.add_favorite(
        testuser_info.get('username'), testuser_info.get('favorite'))
    inserted_fav2 = favorites_dbo.add_favorite(
        testuser_info.get('username'), testuser_info.get('favoriteTwo'))

    if not (inserted_user and inserted_fav1 and inserted_fav2):
        raise Exception('test not set up properly')

    assertEqual(favorites_dbo.remove_all_favorites(
        testuser_info.get("username")), True)

    if not user_dbo.delete_user(testuser_info.get("username"), testuser_info.get("passwordChange"), favorites_dbo):
        raise Exception('test not cleaned up properly')


def run_user_dbo_tests(cur, conn):
    user_dbo = users.UsersTable(cur, conn)
    user_dbo_tests = [
        test_insert_delete_user,
        test_duplicate_insert_user,
        test_authenticate_user,
        test_change_password
    ]

    failed_tests = 0
    for test in user_dbo_tests:
        try:
            test(user_dbo)
        except AssertionError:
            failed_tests += 1

    return len(user_dbo_tests), failed_tests


def test_duplicate_insert_user(user_dbo: users.UsersTable):
    assertEqual(user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    assertEqual(user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("password")), False)
    if not user_dbo.delete_user(testuser_info.get("username"), testuser_info.get("password"), favorites.FavoritesTable()):
        raise Exception('test not cleaned up properly')


def test_insert_delete_user(user_dbo: users.UsersTable):
    assertEqual(user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    assertEqual(user_dbo.delete_user(testuser_info.get("username"),
                                     testuser_info.get("password"), favorites.FavoritesTable()), True)


def test_authenticate_user(user_dbo: users.UsersTable):
    assertEqual(user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    assertEqual(user_dbo.authenticate_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    if not user_dbo.delete_user(testuser_info.get("username"), testuser_info.get("password"), favorites.FavoritesTable()):
        raise Exception('test not cleaned up properly')


def test_change_password(user_dbo: users.UsersTable):
    assertEqual(user_dbo.insert_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    assertEqual(user_dbo.authenticate_user(testuser_info.get(
        "username"), testuser_info.get("password")), True)
    assertEqual(user_dbo.change_user_password(
        testuser_info.get("username"), testuser_info.get("password"), testuser_info.get("passwordChange")), True)
    assertEqual(user_dbo.authenticate_user(testuser_info.get(
        "username"), testuser_info.get("passwordChange")), True)
    if not user_dbo.delete_user(testuser_info.get("username"), testuser_info.get("passwordChange"), favorites.FavoritesTable()):
        raise Exception('test not cleaned up properly')


def assertEqual(actual, expected):
    if actual != expected:
        raise AssertionError(
            'actual {} doesn\'t equal expected {}'.format(actual, expected))


if __name__ == '__main__':
    run_all_db_tests()