# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# test/test_trader.py
#

import logging
import unittest
from unittest import mock

from odoo_client import OdooClient
from trader import Trader

class TddTrader(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    @mock.patch("odoo_client.OdooClient")
    def test_trader_object(self, mock_OdooClient):

        odoo_client = mock_OdooClient.return_value
        odoo_client.get_trader.return_value = {"exchange": {"name":"FTX"}, "market": {"name": "BTC"}}
        
        instance = Trader(odoo_client)
        self.assertIsInstance(instance, Trader)

        trader_data = instance.get_trader_data(1)
        self.assertEqual(trader_data.get("exchange").get("name"), "FTX")
                
        return

    
