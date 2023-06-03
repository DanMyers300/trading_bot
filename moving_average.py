"""A moving average trading bot"""
import time
from datetime import datetime, time as dt_time
from dotenv import load_dotenv
from alpaca_trade_api import REST
import numpy as np

load_dotenv()

ALPACA_API_KEY = os.getenv('API_KEY')
ALPACA_SECRET_KEY = os.getenv('SECRET_KEY')
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL']  # List of symbols to trade

api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY)

def check_trading_condition(symbol):
    # Fetch stock data for the symbol
    stock_data = api.get_barset(symbol, 'day', limit=100).df

    # Calculate moving averages
    stock_data['20_SMA'] = stock_data[symbol]['close'].rolling(window=20, min_periods=1).mean()
    stock_data['10_SMA'] = stock_data[symbol]['close'].rolling(window=10, min_periods=1).mean()

    # Check for crossover points
    stock_data['Cross'] = np.where(stock_data['10_SMA'] > stock_data['20_SMA'], 1.0, 0.0)
    stock_data['Signal'] = stock_data['Cross'].diff()

    # Map numbers to words
    map_dict = {-1.0: 'sell', 1.0: 'buy', 0.0: 'none'}
    stock_data["Signal"] = stock_data["Signal"].map(map_dict)

    # Get the latest signal
    latest_signal = stock_data.iloc[-1]['Signal']

    return latest_signal

def is_trading_hours():
    now = datetime.now().time()
    start_time = dt_time(9, 30)  # Trading starts at 9:30 AM
    end_time = dt_time(16)  # Trading ends at 4:00 PM

    return start_time <= now <= end_time

while True:
    if not is_trading_hours():
        print("Outside trading hours")
        time.sleep(60)  # Sleep for 60 seconds before checking again
        continue

    for symbol in SYMBOLS:
        try:
            trading_condition = check_trading_condition(symbol)
            if trading_condition == 'buy':
                # Place a buy order
                api.submit_order(
                    symbol=symbol,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Bought {symbol}")
            elif trading_condition == 'sell':
                # Place a sell order to close the position
                api.submit_order(
                    symbol=symbol,
                    qty=1,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Sold {symbol}")
            else:
                print(f"Holding {symbol}")
        except Exception as e:
            print(f"Error occurred for {symbol}: {str(e)}")
    time.sleep(60)  # Sleep for 60 seconds before checking again
