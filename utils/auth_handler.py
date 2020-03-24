from datetime import datetime as dt
from database_objects import tools


class AuthHandler:
    def __init__(self):
        self.auth_tokens = {}

    def get_auth_token(self, username):
        auth_token = tools.encode('{}{}'.format(username, random.randint(0, 20)))
        self.auth_tokens[auth_token] = dt.now()
        return auth_token, self.auth_tokens.get(auth_token)

    def is_authenticated_request(self, request):
        auth_type, auth_token = request.headers.get("Authorization").split()
        return auth_token == "Bearer" and is_token_valid(auth_token)

    def is_token_valid(self, auth_token):
        self.remove_timed_out_tokens()
        if auth_token in self.auth_tokens.keys():
            AUTH_TOKENS[auth_token] = dt.now()
            return True
        return False

    def remove_timed_out_tokens(self):
        tokens_to_remove = []
        for token, time in self.auth_tokens.items():
            if (dt.now() - time).seconds > 1800:
                tokens_to_remove.append(token)
        for t in tokens_to_remove:
            del self.auth_tokens[t]
