# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trade/trader.py
#

import os
import sys
import logging

from odoo_client import OdooClient
from ftx_exchange import FtxExchange
from dydx_exchange import DydxExchange
from mxc_exchange import MxcExchange


class Trader():
    def __init__(self, odoo_client):
        self.odoo_client = odoo_client
        self.trader_data = None
        self.exchange = None
        return

    def get_exchange(self, name):
        name = name.lower()
        if name == "mxc":
            return MxcGridExchange(self)
        if name == "dydx":
            return DydxExchange(self)
        if name == "ftx":
            return FtxExchange(self)
        logging.error("No exchange for [%s]" % name)
        return None

    def get_trader_data(self, trader_id):        
        trader_data = self.odoo_client.get_trader(trader_id)
        if not trader_data:
            return None        
        return trader_data

    def init_exchange(self, trader_data):
        exchange_data = trader_data.get("exchange")
        if not exchange_data:
            return None
        exchange = self.get_exchange(exchange_data.get("name"))
        if not exchange:
            return None
        exchange.init_with_exchange_data(exchange_data)
        return exchange

    def loop(self):
        while True:
            time.sleep(1)
            logging.info("In trader loop")
        return

    # def init_market(self, trader_data):
    #     market_data = trader_data.get("market")
    #     if not market_data:
    #         return None
    #     market = get_market(market_data)
    #     if not market:
    #         return None
    #     return market

        

