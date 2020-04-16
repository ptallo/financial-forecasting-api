import random

from datetime import datetime as dt
from database_objects import tools, dbcontext


class AuthHandler:
    def __init__(self, context: dbcontext.DatabaseContext, timeout_length=1800):
        self.context = context
        self.timeout_length = timeout_length

    def get_auth_token(self, username):
        # check if token is still valid, if so return that token
        if self.context.auth_tokens.get_row_for_username(username):
            _, token, _ = self.context.auth_tokens.get_row_for_username(username)
            if not self.is_token_timedout(token):
                return self.context.auth_tokens.get_row_for_username(username)

        # else return newly updated token
        self.gen_new_token(username)
        return self.context.auth_tokens.get_row_for_username(username)

    def gen_new_token(self, username):
        token = tools.encode('{}{}{}'.format(
            username, dt.now().strftime("%m%d%Y%H%M%S"), random.randint(0, 10000)))
        self.context.auth_tokens.insert_token(username, token)
        self.context.save()

    def is_token_timedout(self, token):
        return self.context.auth_tokens.is_token_timedout(token)

    def is_token_valid(self, token):
        return token in self.context.auth_tokens.get_all_tokens()

    def is_authenticated_request(self, request):
        auth_type, auth_token = request.headers.get("Authorization").split()
        if auth_type != "Bearer":
            return False
        elif not self.is_token_valid(auth_token):
            return False
        return not self.is_token_timedout(auth_token)

    def get_user(self, request):
        _, auth_token = request.headers.get("Authorization").split()
        username, token, time = self.context.auth_tokens.get_row_for_token(auth_token)
        return username
