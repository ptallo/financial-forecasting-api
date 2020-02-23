# app.py
from flask import Flask, request, jsonify, flash, abort
from flask_cors import *

from iexfinance.stocks import *
from datetime import datetime as dt
import random
import database_functions

app = Flask(__name__)
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"

CORS(app, origins='*')

AUTH_TOKENS = {}

@app.route('/getstockinfo/', methods=['GET'])
def respond():
    # TODO : get auth token here and check
    authtoken = request.args.get("authtoken", type=str)
    if not check_auth(authtoken):
        abort(400, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("stock", type=str)
    raw_start = request.args.get("start", type=str)
    raw_end = request.args.get("end", type=str)

    # List comprehension to make start date
    sl = [int(x) for x in str.split(raw_start, "-")]
    # List comprehension to make end date
    el = [int(x) for x in str.split(raw_end, "-")]

    # Start date built from sl code comprehension
    start_date = dt(sl[0], sl[1], sl[2])
    # End date built from el code comprehension
    end_date = dt(el[0], el[1], el[2])

    # Grab data from stock (ticker) from last end_date-start_date days
    data = get_historical_data(ticker, start_date, end_date)

    # Extract date keys from historical data
    vals = [data[key]["close"] for key in data.keys()]
    # Put Dates and Close values into response
    response = {"x": list(data.keys()), "y": [vals], "names": ["actual"]}

    # Return the response in json format
    return jsonify(response)


@app.route('/signup/', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    status, message = database_functions.insert_user(username, password)
    return message, status

@app.route('/login/', methods=['GET'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    should_auth_user = database_functions.auth_user(username, password)
    if should_auth_user:
        auth_token, auth_time = generate_auth_token(username)
        AUTH_TOKENS[auth_token] = auth_time
        response_dict = {
            "token": auth_token,
            "time": auth_time
        }
        return jsonify(response_dict)
    else:
        abort(400)

def generate_auth_token(username):
    thing_to_hash = 'username{}'.format(random.randint(0, 20))
    return database_functions.encode(thing_to_hash), dt.now()

def check_auth(auth_token):
    tokens_to_remove = []
    for token, time in AUTH_TOKENS.items():
        if (dt.now() - time).seconds > 1800:
            tokens_to_remove.append(token)
    for t in tokens_to_remove:
        del AUTH_TOKENS[t]
    return auth_token in AUTH_TOKENS  



if __name__ == '__main__':
    app.run(threaded=True, port=5000)

