import random

from datetime import datetime as dt
from database_objects import tools, dbcontext

class AuthHandler:
    def __init__(self, context):
        self.context = context
        self.auth_tokens = {}
        self.init_tokens()

    def init_tokens(self):
        self.remove_timed_out_tokens()
        tokens = self.context.auth_tokens.get_all_tokens()
        for user, token in tokens:
            self.add_auth_token(user, token)

    def add_auth_token(self, username, auth_token):
        self.auth_tokens[auth_token] = {"time_out": dt.now(), "user": username}
        self.context.auth_tokens.add_token(username, auth_token)
        self.context.save()
        return

    def get_auth_token(self, username):
        auth_token = tools.encode('{}{}'.format(
            username, random.randint(0, 20)))
        self.add_auth_token(username, auth_token)
        return auth_token, self.auth_tokens.get(auth_token)

    def is_authenticated_request(self, request):
        auth_type, auth_token = request.headers.get("Authorization").split()
        return auth_type == "Bearer" and self.is_token_valid(auth_token)

    def get_user(self, request):
        _, auth_token = request.headers.get("Authorization").split()
        time_user_dict = self.auth_tokens[auth_token]
        return time_user_dict["user"]

    def is_token_valid(self, auth_token):
        self.remove_timed_out_tokens()
        if auth_token in self.auth_tokens.keys():
            self.auth_tokens[auth_token]["time_out"] = dt.now()
            return True
        return False

    def remove_timed_out_tokens(self):
        tokens_to_remove = []
        for token, time_user_dict in self.auth_tokens.items():
            time = time_user_dict["time_out"]
            if (dt.now() - time).seconds > 1800:
                tokens_to_remove.append(token)
        for t in tokens_to_remove:
            del self.auth_tokens[t]
