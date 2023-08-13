from flask import Flask, render_template, jsonify, request
import pandas as pd
from Essentials import Essentials
from datetime import datetime, timedelta

app = Flask(__name__)

# Assuming you already have a pandas DataFrame named 'df' with the required columns

symbol_list = ["NSE:NIFTY50-INDEX", "NSE:NIFTY2370619200CE", "NSE:NIFTY2370619050PE"]
time_frame_list = ["1", "2", "3", "5", "10", "15", "20", "30", "60", "120", "240", "D"]

symbol = symbol_list[0]
time_frame = time_frame_list[0]


@app.route('/')
def index():
    symbol_list = ["NSE:NIFTY50-INDEX", "NSE:NIFTY2370619300CE", "NSE:NIFTY2370619200PE"]
    time_frame_list = ["1", "2", "3", "5", "10", "15", "20", "30", "60", "120", "240", "D","W","M"]

    symbol = symbol_list[0]
    time_frame = time_frame_list[0]

    return render_template('index.html', symbol=symbol, time_frame=time_frame, symbol_list=symbol_list,
                           time_frame_list=time_frame_list)


__QUANTITY__ = 50

@app.route('/buyCall')
def buyCall():
    order = Essentials.create_market_order(symbol_list[1], __QUANTITY__, 'buy')
    print(order)
    return jsonify(order=order)

@app.route('/sellCall')
def sellCall():
    order = Essentials.create_market_order(symbol_list[1], __QUANTITY__, 'sell')
    print(order)
    return jsonify(order=order)

@app.route('/buyPut')
def buyPut():
    order = Essentials.create_market_order(symbol_list[2], __QUANTITY__, 'buy')
    print(order)
    return jsonify(order=order)

@app.route('/sellPut')
def sellPut():
    order = Essentials.create_market_order(symbol_list[2], __QUANTITY__, 'sell')
    print(order)
    return jsonify(order=order)




@app.route('/data')
def data():
    global symbol
    global time_frame

    symbol = request.args.get('symbol') or symbol
    time_frame_param = request.args.get('time_frame')
    time_frame = time_frame_param or time_frame

    range_from = int(datetime.timestamp(datetime.now() - timedelta(days=10)))
    range_to = int(datetime.timestamp(datetime.now()))

    data = Essentials.historical_data(symbol, time_frame, 0, range_from, range_to, 1)
    data = data['candles']
    data = pd.DataFrame(data)
    data.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')  # Convert timestamp to datetime

    candlestick_data = []

    for index, row in data.iterrows():
        candle = {
            "time": int(datetime.timestamp(row['Timestamp'])) * 1000,  # Convert datetime to milliseconds timestamp
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close']
        }
        candlestick_data.append(candle)

    return jsonify(candlestick_data)



if __name__ == '__main__':
    app.run(debug=True)
