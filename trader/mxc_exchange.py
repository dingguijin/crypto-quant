import os

import logging
import math
import time
import datetime
import itertools
import random

from enum import Enum
from dotenv import load_dotenv
load_dotenv()

import pprint

from mxc_client import MxcClient
from trade_side import TradeSide
from trade_type import TradeType

class MxcMarket(Enum):
    BTC = "BTC_USDT"
    ETH = "ETH_USDT"
    APN = "APN_USDT"
    ZHT = "ZHT_USDT"

class MxcTradeSide(Enum):
    BUY = "BID"
    SELL = "ASK"

class MxcTradeType(Enum):
    MARKET = "IMMEDIATE_OR_CANCEL"
    LIMIT = "LIMIT_ORDER"

class MxcExchange():

    def __init__(self, market=MxcMarket.APN.value, size=0.001):
        self.market = market
        self.size = size
        self.client = self._init_client()
        return

    def _init_client(self):
        _key = os.getenv("WWP_MXC_API_KEY")
        _secret = os.getenv("WWP_MXC_API_SECRET")

        #_key = os.getenv("MXC_API_KEY")
        #_secret = os.getenv("MXC_API_SECRET")

        return MxcClient(api_key=_key, api_secret=_secret)

    def place_market_order(self, side, price):
        return self.place_order(side, price, MxcTradeType.MARKET)

    def place_limit_order(self, side, price):
        return self.place_order(side, price, MxcTradeType.LIMIT)

    def place_order(self, side, price, order_type):

        size = random.randint(500, 1000)
        order_response = self.client.place_order(self.market, price, size,
                                                 side.value, order_type.value)
        if not order_response:
            logging.error("create order return None")
            return None

        logging.info("place %s order: %s response id: %s" % (side, price, order_response))
        return {"status": "placed",
                "order_id": order_response,
                "price": price}

    def cancel_orders(self, order_ids):
        logging.info("canceling orders : %s" % order_ids)
        try:
            for order in order_ids:
                self.client.cancel_orders(order)
            #self.client.cancel_orders(",".join(order_ids[:5]))            
        except Exception as e:
            logging.error("cancel %s meet e: %s" % (order_ids, e))
            return 
        return order_ids

    def get_last_trade(self):
        future = self.client.list_trades(self.market, limit=1)[0]
        return {"price": float(future.get("trade_price"))}

    def get_fills(self, limit=4):
        fills = self.client.list_fills(self.market, limit=limit)
        if not fills:
            logging.error("no fills")
            return []
        
        fills = filter(lambda x: x.get("market") == self.market, fills)
        fills = list(map(lambda x: {
            "order_id": x.get("orderId"),
            "price": x.get("price")
        }, fills))
        
        return fills[:limit]

    def get_open_orders(self):
        orders = self.client.get_open_orders(market=self.market)
        if not orders:
            return []
        orders = list(filter(lambda x: x.get("state") == "NEW", orders))
        for order in orders:
            order.update({"order_id": order.get("id")})
        return orders

    def get_open_positions(self):
        account_info = self.client.get_account_info()
        if not account_info:
            return []

        base_currency = self.market.split("_")[0]
        if not account_info.get(base_currency):
            return []
        
        return [{"size": float(account_info[base_currency].get("available"))}]

    def get_account_balance(self):
        return None

    def convert_side_for_exchange(self, side):
        if side == TradeSide.SELL:
            return MxcTradeSide.SELL
        if side == TradeSide.BUY:
            return MxcTradeSide.BUY
        return None


def _test_grid_exchange():
    mxc = MxcGridExchange(market=MxcMarket.APN.value, size=1000)
    # symbols = mxc.client.list_symbols()
    # APN_USDT
    # pprint.pprint(list(map(lambda x: x.get("symbol"), symbols)))
    
    #pprint.pprint(mxc.client.list_trades(MxcMarket.BTC.value, limit=1))
    #pprint.pprint(mxc.get_fills(limit=1))
    latest_price = mxc.get_last_trade().get("price")
    order = mxc.place_limit_order(MxcTradeSide.BUY, latest_price*0.50)

    time.sleep(2)

    mxc.cancel_orders([order.get("order_id")])
    return


def _test_trend_following():
    mxc = MxcGridExchange(market=MxcMarket.APN.value, size=1000)
    klines = mxc.client.get_klines(market=MxcMarket.BTC.value, interval="1m", limit=100)
    pprint.pprint(klines)
    
    return


if __name__ == "__main__":
    import os
    import sys
    import logging

    _root_dir = os.path.join(os.path.dirname(__file__), "../../")
    sys.path.append(os.path.abspath(_root_dir))

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    mxc = MxcGridExchange(market=MxcMarket.ZHT.value, size=1000)
    account_info = mxc.client.get_account_info()
    pprint.pprint(account_info)

    open_orders = mxc.get_open_orders()
    pprint.pprint(open_orders)

    # _start_grid_loop()
    # _test_grip_price_list()
    # _test_grid_exchange()
    # _test_trend_following()
