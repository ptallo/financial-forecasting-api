# app.py
from flask import Flask, request, jsonify
import datetime as dt

app = Flask(__name__)

@app.route('/getstockinfo/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    ticker = request.args.get("Stock")
    startDate = request.args.get("Start")
    endDate = request.args.get("Start")

    response = {}

    dates = [dt.date(2018, 5, 1),
             dt.date(2018, 5, 2),
             dt.date(2018, 5, 3),
             dt.date(2018, 5, 4),
             dt.date(2018, 5, 5),
             dt.date(2018, 5, 6),
             dt.date(2018, 5, 7)]

    response["x"] = dates

    y = {}
    y["model1"] = [100.34, 95.67, 103.88, 120.55, 75.98, 80.65, 89.13]
    y["actual"] = [100.00, 80.55, 60.99, 170.88, 120.70, 99.00, 77.77]

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
