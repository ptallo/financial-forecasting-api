# app.py
from flask import Flask, request, jsonify, flash
from flask_login import current_user, login_user, LoginManager
from flask_httpauth import HTTPAuth
from flask_cors import *
from iexfinance.stocks import *
from datetime import datetime as dt
from user import User as user

app = Flask(__name__)
auth = HTTPAuth()
login_manager = LoginManager()
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"
login_manager.init_app(app)
app.run(threaded=True, port=5000)
CORS(app, origins='*')


@app.route('/getstockinfo/', methods=['GET'])
def respond():
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
    response = {"x": list(data.keys()), "y": vals}

    # Return the response in json format
    return jsonify(response)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    user_name = auth.username()
    pw = auth.get_password(user_name)
    usr = user(user_name, pw)

    if current_user.is_authenticated:
        flash("USER LOGGED IN ALREADY")
        flash("USER LOGGED IN ALREADY")

    if usr.is_authenticated:
        flash("Login Successful")
        print("Login Successful")
        login_user(usr)
    else:
        flash("Incorrect username and password!")
        print("Incorrect username and password!")

    return "Hello"

@login_manager.user_loader
def load_user(user_id):
    return user.get_id(user_id)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


# if __name__ == '__main__':
#     # Threaded option to enable multiple instances for multiple user access support


