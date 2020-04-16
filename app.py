# app.py
from flask import Flask, request, jsonify, flash, abort
from flask_cors import *

import base64

from database_objects.dbcontext import DatabaseContext
from utils.auth_handler import AuthHandler
from utils.iex_handler import IEXHandler

app = Flask(__name__)
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"
CORS(app, origins='*')

dbcontext = DatabaseContext()
auth_handler = AuthHandler(dbcontext)
iex_handler = IEXHandler()

@app.route('/signup/', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if dbcontext.users.insert_user(username, password):
        dbcontext.save()
        return "Signup successful", 200
    else:
        return "Signup failed due to internal server error", 500


@app.route('/login/', methods=['GET'])
def login():
    auth_type, auth_header = request.headers.get("Authorization").split()
    auth_header_str = base64.b64decode(auth_header).decode('utf-8')
    username, password = auth_header_str.split(":")
    if dbcontext.users.authenticate_user(username, password):
        token, time_user_dict = auth_handler.get_auth_token(username)
        time = time_user_dict["time_out"]
        response_dict = {"token": token, "time": time}
        return jsonify(response_dict)
    else:
        return abort(401)


@app.route('/addfavorite/', methods=['POST'])
def add_favorite():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("ticker", type=str)
    username = auth_handler.get_user(request)

    if dbcontext.favorites.add_favorite(username, ticker):
        dbcontext.save()
        return jsonify(dbcontext.favorites.get_all_favorites(username))
    return "Failed to add {} to favorites".format(ticker), 500


@app.route('/delfavorite/', methods=['DELETE'])
def remove_favorite():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("ticker", type=str)
    username = auth_handler.get_user(request)

    if dbcontext.favorites.remove_favorite(username, ticker):
        dbcontext.save()
        return jsonify(dbcontext.favorites.get_all_favorites(username))
    return "Failed to remove {} from favorites".format(ticker), 500


@app.route('/getfavorites/', methods=['GET'])
def get_favorites():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")
    return jsonify(dbcontext.favorites.get_all_favorites(auth_handler.get_user(request)))


@app.route('/getstockinfo/', methods=['GET'])
def respond():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("stock", type=str)
    date_range = request.args.get("daterange", type=str)

    # Grab data from stock (ticker) from last end_date-start_date days
    data = {}

    iex_status_code, iex_return_data = iex_handler.get_historical_data(
        ticker, date_range)
    if iex_status_code != 200:
        abort(iex_status_code, iex_return_data)
    else:
        data = iex_return_data

    # Extract date keys from historical data
    close_data = [field['close'] for field in data]
    dates = [field['date'] for field in data]
    # Put Dates and Close values into response
    response = {"x": dates, "y": [close_data], "names": ["actual"]}

    # Return the response in json format
    return jsonify(response)


@app.route('/getvalidtickers/', methods=['GET'])
def get_valid_tickers():
    iex_status, iex_data = iex_handler.get_valid_stock_tickers()
    if iex_status == 200:
        return jsonify(iex_data)
    return abort(iex_status, iex_data)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
