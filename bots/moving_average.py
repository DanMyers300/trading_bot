import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

trading_client = TradingClient(API_KEY, SECRET_KEY)
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

SYMBOLS = ['AAPL', 'MSFT', 'GOOGL']  # List of symbols to trade
MA_PERIOD = 50  # Number of periods for the moving average

def calculate_moving_average(symbol):
    """Calculate the moving average for a given symbol"""
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame(15, TimeFrameUnit.Minute)
    )
    historical_data = data_client.get_stock_bars(request_params)
    close_prices = [bar.c for bar in historical_data[symbol]]
    moving_average = sum(close_prices[-MA_PERIOD:]) / MA_PERIOD
    return moving_average

def check_trading_condition(symbol):
    """Check trading condition for a given symbol based on moving averages"""
    moving_average = calculate_moving_average(symbol)
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame(1, TimeFrameUnit.Day)
    )
    historical_data = data_client.get_stock_bars(request_params)
    latest_bar = historical_data[symbol][-1]
    current_price = latest_bar.c
    if current_price > moving_average:
        return True  # Buy
    elif current_price < moving_average:
        return False  # Sell
    else:
        return None  # Hold

for symbol in SYMBOLS:
    try:
        trading_condition = check_trading_condition(symbol)
        if trading_condition is True:
            # Buy logic
            print(f"Buy {symbol}")
        elif trading_condition is False:
            # Sell logic
            print(f"Sell {symbol}")
        else:
            # Hold logic
            print(f"Holding {symbol}")
    except Exception as e:
        print(f"Error occurred for {symbol}: {str(e)}")
