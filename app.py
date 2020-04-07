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
        token, time_user_dict = auth_handler.get_auth_token(username)
        time = time_user_dict["time_out"]
        response_dict = {"token": token, "time": time}
        return jsonify(response_dict)
    else:
        return abort(401)


@app.route('/addfavorite/', methods=['GET'])
def add_favorite():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("ticker", type=str)
    username = auth_handler.get_user(request)

    if dbcontext.favorites.add_favorite(username, ticker):
        return "{} successfully added to favorites".format(ticker)
    return "Failed to add {} to favorites".format(ticker)


@app.route('/delfavorite/', methods=['GET'])
def remove_favorite():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("ticker", type=str)
    username = auth_handler.get_user(request)

    if dbcontext.favorites.remove_favorite(username, ticker):
        return "{} successfully removed from favorites".format(ticker)
    return "Failed to remove {} from favorites".format(ticker)


@app.route('/getfavorites/', methods=['GET'])
def get_favorites():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    username = auth_handler.get_user(request)

    favorites = dbcontext.favorites.get_all_favorites(username)

    return jsonify(favorites)


@app.route('/getstockinfo/', methods=['GET'])
def respond():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    # Retrieve the name from url parameter
    ticker = request.args.get("stock", type=str)
    date_range = request.args.get("date_range", type=str)

    # Grab data from stock (ticker) from last end_date-start_date days
    data = {}
    try:
        data = iex_handler.get_historical_data(ticker, date_range)
    except Exception as e:
        return abort(400, str(e))
    # Extract date keys from historical data
    close_data = [field['close'] for field in data]
    dates = [field['date'] for field in data]
    # Put Dates and Close values into response
    response = {"x": dates, "y": [close_data], "names": ["actual"]}

    # Return the response in json format
    return jsonify(response)


@app.route('/getvalidtickers/', methods=['GET'])
def get_valid_tickers():
    if not auth_handler.is_authenticated_request(request):
        return abort(401, "User not authenticated!")

    return jsonify(iex_handler.stock_tickers)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
