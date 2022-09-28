import time
import datetime
import logging
import requests

from trade_side import TradeSide
from trade_type import TradeType

from singleton import Singleton

class Strategy(metaclass=Singleton):
    def __init__(trader):
        self.trader = trader
        self.sleep_interval = trader.sleep_interval
        self.sleep_seconds = 0
        return

    def strategy_loop_once(self):        
        return

    def get_market_fills(self):
        return
        
    def get_market_position(self):
        return

    def get_market_orders(self):
        return
        
    def get_account_balance(self):
        return
        
    def get_placed_orders(self):
        return
        
    def get_cancelled_orders(self):
        return
            
    def sleep(self):
        time.sleep(self.sleep_interval)
        self.sleep_seconds += self.sleep_interval
        return

    



