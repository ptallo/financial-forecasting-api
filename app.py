# app.py
from flask import Flask, request, jsonify, flash, abort
from flask_cors import *

from datetime import datetime as dt
import random
import requests

from database_objects.dbcontext import DatabaseContext
from database_objects import tools

app = Flask(__name__)
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"
CORS(app, origins='*')

dbcontext = DatabaseContext()

AUTH_TOKENS = {}


@app.route('/signup/', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if dbcontext.users.insert_user(username, password):
        return json.dumps({'success': True}), 200
    else:
        return json.dumps({'success': False}), 422


@app.route('/login/', methods=['GET'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if dbcontext.users.authenticate_user(username, password):
        auth_token, auth_time = generate_auth_token(username)
        AUTH_TOKENS[auth_token] = auth_time
        response_dict = {
            "token": auth_token,
            "time": auth_time
        }
        return jsonify(response_dict)
    else:
        return abort(401)


def generate_auth_token(username):
    return tools.encode('{}{}'.format(username, random.randint(0, 20))), dt.now()


def check_auth(auth_token):
    tokens_to_remove = []
    for token, time in AUTH_TOKENS.items():
        if (dt.now() - time).seconds > 1800:
            tokens_to_remove.append(token)
    for t in tokens_to_remove:
        del AUTH_TOKENS[t]
    if auth_token in AUTH_TOKENS:
        AUTH_TOKENS[auth_token] = dt.now()
        return True
    return False


@app.route('/getstockinfo/', methods=['GET'])
def respond():
    authtoken = request.args.get("authtoken", type=str)
    if not check_auth(authtoken):
        abort(400, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("stock", type=str)

    # Grab data from stock (ticker) from last end_date-start_date days
    data = get_historical_data(ticker)

    # Extract date keys from historical data
    vals = [field['close'] for field in data]
    dates = [field['date'] for field in data]
    # Put Dates and Close values into response
    response = {"x": dates, "y": [vals], "names": ["actual"]}

    # Return the response in json format
    return jsonify(response)


def get_historical_data(ticker, drange="3m"):
    # TODO : replace sandbox with live api keys and base url
    base_url = "https://sandbox.iexapis.com"
    request_url = "{}/stable/stock/{}/chart/{}?token={}".format(
        base_url, ticker, drange, "Tsk_942768a24d244db38c7a44e32e3bc000")
    response = requests.get(request_url)
    return response.json()


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
