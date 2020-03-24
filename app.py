# app.py
from flask import Flask, request, jsonify, flash, abort
from flask_cors import *

import base64
import random
import requests

from database_objects.dbcontext import DatabaseContext
from utils.auth_handler import AuthHandler
from utils.iex_handler import IEXHandler

app = Flask(__name__)
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"
CORS(app, origins='*')

dbcontext = DatabaseContext()
auth_handler = AuthHandler()
iex_handler = IEXHandler()


@app.route('/signup/', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if dbcontext.users.insert_user(username, password):
        return "Signup successful", 200
    else:
        return "Signup failed due to internal server error", 422


@app.route('/login/', methods=['GET'])
def login():
    auth_type, auth_header = request.headers.get("Authorization").split()
    auth_header_str = base64.b64decode(auth_header).decode('utf-8')
    username, password = auth_header_str.split(":")
    if dbcontext.users.authenticate_user(username, password):
        token, time = auth_handler.get_auth_token(username)
        response_dict = {"token": token, "time": time}
        return jsonify(response_dict)
    else:
        return abort(401)


@app.route('/getstockinfo/', methods=['GET'])
def respond():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("stock", type=str)

    # Grab data from stock (ticker) from last end_date-start_date days
    data = iex_handler.get_historical_data(ticker)

    # Extract date keys from historical data
    close_data = [field['close'] for field in data]
    dates = [field['date'] for field in data]
    # Put Dates and Close values into response
    response = {"x": dates, "y": [close_data], "names": ["actual"]}

    # Return the response in json format
    return jsonify(response)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
