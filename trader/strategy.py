import time
import datetime
import logging
import requests

from trade_side import TradeSide
from trade_type import TradeType

from singleton import Singleton

class Strategy(metaclass=Singleton):
    def __init__(self, trader):
        self.trader = trader
        self.sleep_interval = trader.trader_data.get("sleep_interval")
        self.market = self.trader.market_data.get("symbol")

        self.sleep_seconds = 0
        self.strategy_data = None
        return

    def init_with_strategy_data(self, strategy_data):
        self.strategy_data = strategy_data
        return
        
    def strategy_loop_once(self):        
        raise NotImplementedError
            
    def sleep(self):
        time.sleep(self.sleep_interval)
        self.sleep_seconds += self.sleep_interval
        return

    



