from database_objects import users
from database_objects import favorites
from database_objects import auth_tokens
from database_objects import dbcontext


test_user = {
    "username": "testuser",
    "password": "chrisisdumb",
    "passwordChange": "ma22ispoopoo",
    "favorite": "AAPL",
    "favoriteTwo": "TSLA"
}

def run_all_db_tests():
    tests = [
        test_insert_user,
        test_delete_user,
        test_change_password,
        test_add_favorite,
        test_remove_favorite,
        test_remove_all_favorites
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError:
            failed.append(test.__name__)

    if len(failed) == 0:
        print("all tests passed!")
    else:
        print("The following tests failed:")
        for f in failed:
            print("  {}".format(f))


def test_insert_user():
    dbc = dbcontext.DatabaseContext()
    insert_successful = dbc.users.insert_user(
        test_user.get("username"), test_user.get("password"))
    assertEqual(insert_successful, True)


def test_delete_user():
    dbc = dbcontext.DatabaseContext()

    dbc.users.insert_user(test_user.get("username"), test_user.get("password"))
    dbc.favorites.add_favorite(test_user.get(
        "username"), test_user.get("favorite"))
    dbc.favorites.add_favorite(test_user.get(
        "username"), test_user.get("favoriteTwo"))

    delete_succesful = dbc.users.delete_user(
        test_user.get("username"), dbc.favorites)

    assertEqual(delete_succesful, True)


def test_change_password():
    dbc = dbcontext.DatabaseContext()

    dbc.users.insert_user(test_user.get("username"), test_user.get("password"))
    change_succesful = dbc.users.change_user_password(
        test_user.get("username"),
        test_user.get("password"),
        test_user.get("passwordChange"))
    assertEqual(change_succesful, True)


def test_add_favorite():
    dbc = dbcontext.DatabaseContext()

    dbc.users.insert_user(test_user.get("username"), test_user.get("password"))
    add_success = dbc.favorites.add_favorite(
        test_user.get("username"),
        test_user.get("favorite"))

    assertEqual(add_success, True)


def test_remove_favorite():
    dbc = dbcontext.DatabaseContext()

    dbc.users.insert_user(test_user.get("username"), test_user.get("password"))

    dbc.favorites.add_favorite(
        test_user.get("username"),
        test_user.get("favorite"))

    del_success = dbc.favorites.remove_favorite(
        test_user.get("username"),
        test_user.get("favorite"))

    assertEqual(del_success, True)


def test_remove_all_favorites():
    dbc = dbcontext.DatabaseContext()

    dbc.users.insert_user(
        test_user.get("username"),
        test_user.get("password"))

    dbc.favorites.add_favorite(
        test_user.get("username"),
        test_user.get("favorite"))

    dbc.favorites.add_favorite(
        test_user.get("username"),
        test_user.get("favoriteTwo"))

    del_all_success = dbc.favorites.remove_all_favorites(
        test_user.get("username"))

    assertEqual(del_all_success, True)


def assertEqual(actual, expected):
    if actual != expected:
        raise AssertionError(
            'actual {} doesn\'t equal expected {}'.format(actual, expected))


if __name__ == '__main__':
    run_all_db_tests()
