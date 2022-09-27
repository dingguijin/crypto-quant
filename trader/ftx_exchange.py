import os

import math
import time
import datetime
import itertools
import logging

from enum import Enum
from dotenv import load_dotenv
load_dotenv()

import pprint

from ftx_client import FtxClient
from trade_side import TradeSide
from trade_type import TradeType


class FtxTradeSide(Enum):
    BUY = "buy"
    SELL = "sell"

class FtxTradeType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class FtxExchange():

    def __init__(self, account_name=None, subaccount_name=None):
        self.account_name = account_name
        self.subaccount_name = subaccount_name
        self.client = self._init_client()
        return

    def _init_client(self):
        _ftx_api_key = "FTX_API_KEY"
        _ftx_api_serect = "FTX_API_SECRET"
        if self.account_name:
            _ftx_api_key = self.account_name + "_" + _ftx_api_key
            _ftx_api_serect = self.account_name + "_" + _ftx_api_serect
        _key = os.getenv(_ftx_api_key)
        _secret = os.getenv(_ftx_api_serect)
        return FtxClient(api_key=_key, api_secret=_secret, subaccount_name=self.subaccount_name)

    def place_conditional_order(self, market, side, size, type="stop",
                                limit_price=None, reduce_only=False,
                                cancel=True, trigger_price=None, trail_value=None):
        return self.client.place_conditional_order(market, side.value, size, type,
                                                   limit_price, reduce_only,
                                                   cancel, trigger_price, trail_value)

    def place_market_order(self, market, size, side, price):
        return self.place_order(market, size, side, price, FtxTradeType.MARKET)

    def place_limit_order(self, market, size, side, price):
        return self.place_order(market, size, side, price, FtxTradeType.LIMIT)

    def place_order(self, market, size, side, price, order_type):
        ioc = False
        post_only = False
        
        if order_type == FtxTradeType.MARKET:
            price = None
        
        try:
            order_response = self.client.place_order(market, side.value, price, size,
                                                    type=order_type.value, reduce_only=False,
                                                    ioc=ioc, post_only=post_only)
        except Exception as e:
            logging.error("create order meet e: %s" % e)
            return None
            
        if not order_response:
            logging.error("create order return None")
            return None

        logging.info("place %s order: %s response id: %s" % (side, price, order_response.get("id")))
        return {"status": "placed",
                "order_id": order_response.get("id"),
                "size": size,
                "side": side.value,
                "price": price}
    
    def cancel_orders(self, order_ids):
        logging.info("cancel_orders order_ids: %s" % order_ids)

        for order_id in order_ids:
            logging.info("canceling order : %s" % order_id)
            try:
                self.client.cancel_order(order_id)
            except Exception as e:
                logging.error("cancel %s meet e: %s" % (order_id, e))
                continue
        return

    def get_last_trade(self, market):
        future = self.client.get_market(market)
        return {"price": float(future.get("last"))}

    def get_fills(self, market, limit=4):
        fills = self.client.get_fills(market)
        if not fills:
            return None
        
        fills = list(map(lambda x: {
            "order_id": x.get("orderId"),
            "price": x.get("price")
        }, fills))
        
        return fills[:limit]

    def get_open_orders(self, market):
        orders = self.client.get_open_orders(market)
        orders = list(filter(lambda x: x.get("status") == "open", orders))
        for order in orders:
            order.update({"order_id": order.get("id")})
        return orders

    def get_open_trigger_orders(self, market):
        orders = self.client.get_open_trigger_orders(market)
        orders = list(filter(lambda x: x.get("status") == "open", orders))
        for order in orders:
            order.update({"order_id": order.get("id")})
        return orders

    def get_open_positions(self, market):
        positions = self.client.get_positions()
        if not positions:
            return []
        positions = list(filter(lambda x: x.get("future") == market and x.get("size") > 0, positions))
        positions = list(map(lambda x: dict(x, **{"side": self._convert_side(x.get("side")),
                                                  "break_even_price": float(x.get("recentBreakEvenPrice")),
                                                  "liquidation_price": float(x.get("estimatedLiquidationPrice")),
                                                  "size": x.get("size"),
                                                  "net_size": x.get("netSize")}), positions))
        return positions

    def get_account_balance(self):
        account_info = self.client.get_account_info()
        return {"total_value": account_info.get("totalAccountValue"),
                "total_position": account_info.get("totalPositionSize")}

    def get_historial_prices(self, market, interval, begin_time, end_time):
        return self.client.get_historial_prices(market, interval, begin_time, end_time)

    def _convert_side(self, side):
        if side == FtxTradeSide.SELL.value:
            return TradeSide.SELL
        if side == FtxTradeSide.BUY.value:
            return TradeSide.BUY
        return None

    def convert_side_for_exchange(self, side):
        if side == TradeSide.SELL:
            return FtxTradeSide.SELL
        if side == TradeSide.BUY:
            return FtxTradeSide.BUY
        return None


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
    
    exchange = FtxExchange(subaccount_name="WWP-01")
    pprint.pprint(exchange.client.get_account_info())
    pprint.pprint(exchange.client.get_account_info().get("openMarginFraction"))

    pprint.pprint(exchange.get_open_positions())
    pprint.pprint(exchange.get_open_positions()[0].get("recentPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("unrealizedPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("realizedPnl"))
    
    exchange = FtxExchange(subaccount_name="DGJ-01")
    pprint.pprint(exchange.client.get_account_info())
    pprint.pprint(exchange.client.get_account_info().get("openMarginFraction"))

    pprint.pprint(exchange.get_open_positions())
    pprint.pprint(exchange.get_open_positions()[0].get("recentPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("unrealizedPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("realizedPnl"))    


    pprint.pprint("=============================")
    exchange = FtxExchange()
    pprint.pprint(exchange.client.get_account_info())
    pprint.pprint(exchange.client.get_account_info().get("openMarginFraction"))

    pprint.pprint(exchange.get_open_positions())
    pprint.pprint(exchange.get_open_positions()[0].get("recentPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("unrealizedPnl"))
    pprint.pprint(exchange.get_open_positions()[0].get("realizedPnl"))    
