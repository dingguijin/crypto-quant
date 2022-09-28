# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# test/test_trader.py
#

import os
import logging
import unittest
from unittest import mock
from dotenv import load_dotenv

from odoo_client import OdooClient
from trader import Trader
from exchange import Exchange
from ftx_exchange import FtxExchange
from dydx_exchange import DydxExchange

from 

class TddTrader(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        load_dotenv()
        return

    def tearDown(self):
        return

    @mock.patch("odoo_client.OdooClient")
    def test_trader_object(self, mock_OdooClient):

        odoo_client = mock_OdooClient.return_value
        odoo_client.get_trader.return_value = {"exchange": {
            "name": "FTX",
            "symbol": "FTX",
            "api_key": os.getenv("FTX_API_KEY"),
            "api_secret": os.getenv("FTX_API_SECRET"),
            "subaccount": "GDJ-01",
        }, "market": {
            "name": "ETH-PERP"
            "symbol": "ETH-PERP"
        }, "strategy": {
            "name": "GRID",
            "symbol": "GRID",
            "grid_gap": 0.0001,
            "grid_size": 0.0001
        }}
        
        instance = Trader(odoo_client)
        self.assertIsInstance(instance, Trader)

        trader_data = instance.get_trader_data(1)
        self.assertEqual(trader_data.get("exchange").get("name"), "FTX")

        exchange = instance.init_exchange(trader_data)
        self.assertIsInstance(exchange, FtxExchange)

        strategy = instance.init_strategy(trader_data)
        self.assertIsInstance(strategy, GridStrategy)

        #price = exchange.get_last_trade("ETH-PERP")
        #account = exchange.client.get_account_info()
        #print(account)

        
        #market = instance.init_market(trader_data)
        #self.assertIsInstance(market, Market)
        return

    
