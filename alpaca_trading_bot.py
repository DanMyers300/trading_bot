"""
A simple trading bot 
"""
import os
import time
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

SYMBOLS = ['AAPL', 'MSFT', 'GOOGL']  # List of symbols to trade

def check_trading_condition(symb):
    """Check trading condition for a given symbol"""
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symb)
    latest_quote = data_client.get_stock_latest_quote(request_params)[symb].ask_price
    if latest_quote < 300.0:
        return True  # Buy condition
    elif latest_quote > 320.0:
        return False  # Sell condition
    return None  # Hold condition

while True:
    for symbol in SYMBOLS:
        try:
            trading_condition = check_trading_condition(symbol)
            if trading_condition is True:
                buy_order = trading_client.submit_order(
                    order_data=MarketOrderRequest(
                        SYMBOL=symbol,
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                    )
                )
                print(f"Bought {symbol} at {buy_order.filled_avg_price}")
            elif trading_condition is False:
                sell_order = trading_client.close_position(symbol)
                print(f"Sold {symbol} at {sell_order.filled_avg_price}")
            else:
                print(f"Holding {symbol}")
        # pylint: disable=broad-except
        except Exception as e:
            print(f"Error occurred for {symbol}: {str(e)}")
    time.sleep(60)  # Sleep for 60 seconds before checking again
