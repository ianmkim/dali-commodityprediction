from flask import Flask
from flask import redirect,jsonify, url_for, render_template, request

from flask_sslify import SSLify
from jinja2 import Environment, FileSystemLoader ,PackageLoader, select_autoescape

# module to return predictions
import oracle

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # get the list of previous prices
    input_arr =request.form.getlist('slice[]')
    # a really really bad way to check for types
    try:
        model = int(request.form.get("model"))
    except:
        model = 1
    try:
        timeframe = int(request.form.get("timeframe"))
    except:
        timeframe = 1
    preds = []
    # append predictions based on the timeframe requested
    for _ in range(timeframe):
        preds.append(oracle.predict_next_price(input_arr, model)[0][0])
        input_arr.pop(0)
        input_arr.append(preds[-1])

    return str(preds)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
