import os

import math
import time
import datetime
import itertools
import logging

from enum import Enum
from dotenv import load_dotenv
load_dotenv()

from dydx3 import Client
from dydx3 import constants
from dydx3 import epoch_seconds_to_iso

import pprint

from trade_type import TradeType
from trade_side import TradeSide

ETH_DYDX = constants.MARKET_ETH_USD
BTC_DYDX = constants.MARKET_BTC_USD

class DydxExchange():
    def __init__(self, account_name):
        self.account_name = account_name

        self.expiration_seconds = 24 * 3600
        self.limit_fee = 0.001

        self.client = self._init_client()

        # FIXME: must be call after init client
        self.position_id = self._get_position_id()
        assert(self.position_id)
        return

    def _init_client(self):
        
        _private_key = os.getenv("%s_DYDX_ETH_PRIVATE_KEY" % self.account_name)
        _api_key = os.getenv("%s_DYDX_API_KEY" % self.account_name)
        _api_secret = os.getenv("%s_DYDX_API_SECRET" % self.account_name)
        _api_passphrase = os.getenv("%s_DYDX_API_PASSPHRASE" % self.account_name)
        _stark_private_key = os.getenv("%s_DYDX_STARK_PRIVATE_KEY" % self.account_name)
    
        return Client(host="https://api.dydx.exchange",eth_private_key=_private_key,stark_private_key=_stark_private_key, default_ethereum_address="0x211164B771F7910445E96914E7a4D66a406458d2", api_key_credentials={"key": _api_key, "secret": _api_secret, "passphrase": _api_passphrase})

    def _get_position_id(self):
        account_response = self.client.private.get_account().data
        return account_response['account']['positionId']

    def place_market_order(self, market, size, side, price):
        return self.place_order(market, size, side, price, "MARKET")

    def place_limit_order(self, market, size, side, price):
        return self.place_order(market, size, side, price, "LIMIT")

    def place_order(self, market, size, side, price, order_type):

        order_price = str(price)
        time_in_force = constants.TIME_IN_FORCE_GTT
        if order_type == "MARKET":
            time_in_force = constants.TIME_IN_FORCE_IOC

        # FIXME BTC must be int
        if market == "BTC-USD":
            order_price = str(round(price))
            
        order_params = {
            'position_id': self.position_id,
            'market': market,
            'side': side,
            'order_type': order_type,
            'post_only': False,
            'size': str(size),
            'price': order_price,
            'limit_fee': str(self.limit_fee),
            'time_in_force': time_in_force,
            'expiration_epoch_seconds': round(time.time()) + self.expiration_seconds,
        }

        logging.info("placing order: %s" % order_params)
        
        order_response = self.client.private.create_order(**order_params).data
        if not order_response:
            logging.error("create order return None")
            return None
        
        order = order_response["order"]
        
        logging.info("place order: %s response order_id: %s" % (order_params, order.get("id")))
        return {"status": "placed",
                "order_id": order.get("id"),
                "side": side,
                "size": size,
                "price": price}
    
    def cancel_orders(self, order_ids):
        logging.info("cancel_orders order_ids: %s" % order_ids)

        for order_id in order_ids:
            logging.info("canceling order : %s" % order_id)
            try:
                self.client.private.cancel_order(order_id)
            except Exception as e:
                logging.error("cancel %s meet e: %s" % (order_id, e))
                continue
        return

    def get_last_trade(self, market):
        uri = '/'.join(['/v3/trades', market])
        trades = self.client.public._get(
            uri,
            {'limit': 1},
        ).data
        trades = trades["trades"][0]
        return {"side": trades.get("side"),
                "price": float(trades.get("price"))}

    def get_fills(self, market, limit=4):
        fills = self.client.private.get_fills(market=market, limit=limit).data
        fills = fills.get("fills")        
        fills = list(map(lambda x: {
            "size": x.get("size"),
            "side": x.get("side"),
            "order_id": x.get("orderId"),
            "price": x.get("price")}, fills))
        return fills

    def get_open_orders(self, market):
        orders = self.client.private.get_orders(market=market,
                                                status=constants.ORDER_STATUS_OPEN,
                                                order_type=constants.ORDER_TYPE_LIMIT).data

        logging.info("dydx get_open_orders %s" % orders)
        if not orders:
            return []
        
        orders = orders["orders"]
        orders = list(filter(lambda x: x.get("status") == "OPEN" and x.get("market") == market, orders))

        for order in orders:
            order.update({"order_id": order.get("id")})
        return orders

    # 余额 = 持仓 * （持仓均价 - 清算价） IF LONG
    def _get_liquidation_price(self, pos, account):
        _side = pos.get("side")
        _equity = float(account.get("equity"))
        _size = abs(float(pos.get("size")))
        _break_even_price = self._get_break_even_price(pos)
        _unrealizedPnl = float(pos.get("unrealizedPnl"))
        _realizedPnl = float(pos.get("realizedPnl"))
        _equity = _equity - _realizedPnl - _unrealizedPnl
        
        if _side == "LONG":
            return _break_even_price - _equity*0.97/_size
        return _break_even_price + _equity*0.97/_size 

    def _get_break_even_price(self, pos):
        _entryPrice = float(pos.get("entryPrice"))
        _exitPrice = float(pos.get("exitPrice"))
        _sumOpen = float(pos.get("sumOpen"))
        _sumClose = float(pos.get("sumClose"))
        return (_entryPrice * _sumOpen - _exitPrice * _sumClose)/(_sumOpen - _sumClose)
    
    def get_open_positions(self, market):
        account_info = self.client.private.get_account().data.get("account")
        if not account_info:
            return []

        positions = account_info.get("openPositions")        
        if not positions:
            return []

        positions = list(positions.values())
        positions = list(filter(lambda x: x.get("market") == market and abs(float(x.get("size"))) > 0.0, positions))
        positions = list(map(lambda x: dict(x, **{"side": self._convert_side(x.get("side")),
                                                  "net_size": float(x.get("size")),
                                                  "liquidation_price": self._get_liquidation_price(x, account_info),
                                                  "break_even_price": self._get_break_even_price(x),
                                                  "size": abs(float(x.get("size")))}), positions))
        return positions

    def get_account_balance(self):
        account_info = self.client.private.get_account().data
        if not account_info:
            return None
        account_info = account_info.get("account")
        if not account_info:
            return None
        
        total_value = float(account_info.get("equity"))
        quote_balance = float(account_info.get("quoteBalance"))
        total_position = total_value - quote_balance
        return {"total_value": total_value,
                "total_position": total_position}

    def _convert_side(self, side):
        if side == constants.ORDER_SIDE_SELL or "SHORT":
            return TradeSide.SELL
        if side == constants.ORDER_SIDE_BUY or "LONG":
            return TradeSide.BUY
        return None

    def convert_side_for_exchange(self, side):
        if side == TradeSide.SELL:
            return constants.ORDER_SIDE_SELL
        if side == TradeSide.BUY:
            return constants.ORDER_SIDE_BUY
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
        
    exchange = DydxGridExchange()
    pprint.pprint(exchange.client.private.get_account().data)
    pprint.pprint(exchange.get_open_positions())
    pprint.pprint(exchange.get_open_positions()[0].get("unrealizedPnl"))
