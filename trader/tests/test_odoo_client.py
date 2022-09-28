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
from odoo_client import OdooClient

class TddOdooClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_odoo_client_object(self):
        instance = OdooClient(host="localhost", port=8069)
        self.assertIsInstance(instance, OdooClient)
        return


