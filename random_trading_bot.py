"A bot that buys, sells, and holds at random"
import os
import random
import time
from datetime import datetime, time as dt_time
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

SYMBOLS = ['AAPL', 'MSFT', 'GOOGL']  # List of symbols to trade

def check_trading_hours():
    """Check if current time is within trading hours"""
    current_time = datetime.now().time()
    start_time = dt_time(9, 30)  # Assuming trading starts at 9:30 AM
    end_time = dt_time(16, 0)  # Assuming trading ends at 4:00 PM
    return start_time <= current_time <= end_time

def check_trading_condition():
    """Check trading condition for a given symbol"""
    return random.choice([True, False, None])

while True:
    if check_trading_hours():
        for symbol in SYMBOLS:
            try:
                trading_condition = check_trading_condition()
                if trading_condition is True:
                    # Buy logic
                    buy_order = trading_client.submit_order(
                        order_data=MarketOrderRequest(
                            symbol=symbol,
                            qty=1,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY
                        )
                    )
                    print(f"Bought {symbol} at {buy_order.filled_avg_price}")
                elif trading_condition is False:
                    # Sell logic
                    sell_order = trading_client.close_position(symbol)
                    print(f"Sold {symbol} at {sell_order.filled_avg_price}")
                else:
                    # Hold logic
                    print(f"Holding {symbol}")
            # pylint: disable=broad-except
            except Exception as e:
                print(f"Error occurred for {symbol}: {str(e)}")
    else:
        print("Outside trading hours")
    time.sleep(60)  # Sleep for 60 seconds before checking again
