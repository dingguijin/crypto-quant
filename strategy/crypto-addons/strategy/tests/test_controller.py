# -*- coding: utf-8 -*-

from odoo.tests.common import users, TransactionCase

class TestControllerCase(TransactionCase):

    def setUp(self):
        super().setUp()

    def test_update_pnl(self):
        strategy_1 = self.env['mfbot.strategy'].create({
            "strategy": "GRID",
            "market": "BTC",
            "exchange": "FTX",
            "invest": 10000.00
        })
        print(strategy_1)
        return
