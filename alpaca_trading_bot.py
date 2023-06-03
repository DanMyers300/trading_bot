"""
A simple trading bot
"""

import os
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def get_account_information():
    """Getting account information"""
    account = trading_client.get_account()
    for property_name, value in account:
        print(f"\"{property_name}\": {value}")
