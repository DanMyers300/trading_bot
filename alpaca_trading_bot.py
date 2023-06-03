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

# def get_account_information():
#     """Getting account information"""
#     account = trading_client.get_account()
#     for property_name, value in account:
#         print(f"\"{property_name}\": {value}")

# get_account_information()

SYMBOL = 'TSLA'
data_client = StockHistoricalDataClient('<Your API Key>', '<Your API Secret>')
trading_client = TradingClient('<Your API Key>', '<Your API Secret>', paper=True)
while True:
    request_params = StockLatestQuoteRequest(symbol_or_symbols=SYMBOL)
    latest_quote = data_client.get_stock_latest_quote(request_params)[SYMBOL].ask_price
    if latest_quote < 300.0:
        buy_order = trading_client.submit_order(
                                                order_data=MarketOrderRequest(
                                                    SYMBOL=SYMBOL,
                                                    qty=1,
                                                    side=OrderSide.BUY,
                                                    time_in_force=TimeInForce.DAY)
                                                )
    elif latest_quote > 320.0:
        sell_order = trading_client.close_position(SYMBOL)
    time.sleep(60)
