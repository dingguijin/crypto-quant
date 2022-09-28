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
from exchange import get_exchange
from market import get_market

class Trader():
    def __init__(self, odoo_client):
        self.odoo_client = odoo_client
        self.trader_data = {}
        return

    def get_trader_data(self, trader_id):        
        trader_data = self.odoo_client.get_trader(trader_id)
        if not trader_data:
            return None        
        return trader_data

    def init_exchange(self, trader_data):
        exchange_data = trader_data.get("exchange_data")
        if not exchange_data:
            return None
        exchange = get_exchange(exchange_data.get("name"))
        if not exchange:
            return None
        exchange.init_with_exchange_data(exchange_data)
        return exchange
    
    def init_exchange(self, trader_data):
        market_data = trader_data.get("market")
        if not market_data:
            return None
        market = get_market(market_data)
        if not market:
            return None
        return market

        

