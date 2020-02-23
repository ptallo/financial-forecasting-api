# app.py
from flask import Flask, request, jsonify, flash, abort
from flask_cors import *
from flask_login import LoginManager


from iexfinance.stocks import *
from datetime import datetime as dt
from database_functions import auth_user, insert_user

app = Flask(__name__)
app.secret_key = "USSR_SUPPER_SEKRET_KEZ"

login_manager = LoginManager()
login_manager.init_app(app)

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))

def is_safe_url(url):
    return 'financial-forecasting-react' in url

@auth.verify_password
def verify_password(username, password):
    return auth_user(username, password)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

