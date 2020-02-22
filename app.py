# app.py
from flask import Flask, request, jsonify
from iexfinance.stocks import *
from datetime import datetime as dt

app = Flask(__name__)


@app.route('/getstockinfo/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    ticker = request.args.get("Stock", type=str)
    raw_start = request.args.get("Start", type=str)
    raw_end = request.args.get("Start", type=str)

    raw_start = "2019-5-1"
    raw_end = "2019-5-8"
    ticker = "TSLA"

    sl = [int(x) for x in str.split(raw_start, "-")]
    el = [int(x) for x in str.split(raw_end, "-")]

    start_date = dt(sl[0], sl[1], sl[2])
    end_date = dt(el[0], el[1], el[2])

    data = get_historical_data(ticker, start_date, end_date)
    vals = []

    for key in data.keys():
        vals.append(data[key]["close"])

    response = {"x": list(data.keys())}

    y = {}
    y["model1"] = [100.34, 95.67, 103.88, 120.55, 75.98, 80.65, 89.13]
    y["actual"] = vals

    response["y"] = y

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
