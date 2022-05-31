import math

from flask import Flask, render_template, request
from pandas_datareader import data as pdr
from datetime import datetime
import yfinance as yf

yf.pdr_override()

app = Flask(__name__)


# @app.route('/code/', methods=['GET', 'POST'])
# def index_code():
#     if request.method == "POST":
#         print(request.form.get('data'))
#     return "<h1> about </h1>"


def get_data(code, invest):
    date = datetime.now().date()
    initial_investment = invest
    data = pdr.get_data_yahoo(code, start="2017-01-01", end=f"{date}", interval="1mo")
    data = data.dropna(axis=0, how='any')
    stock_price = data['Close'].tolist()
    shares_held = initial_investment // stock_price[0]
    yvalues = list(map(lambda n: n * shares_held, stock_price))
    xvalues = list(x for x in range(0, len(yvalues)))
    years = len(xvalues) / 12

    context = {
        'yvalues': yvalues,
        'xvalues': xvalues,
        'years': math.ceil(years)
    }

    return context


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        code = request.form.get('code')
        value = float(request.form.get('value'))
        context = get_data(code.lower(), value)
        print(context)
        return render_template('main.html', context=context)
    else:
        context = get_data('goog', 50000)
        return render_template('main.html', context=context)
