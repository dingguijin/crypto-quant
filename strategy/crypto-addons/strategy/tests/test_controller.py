# -*- coding: utf-8 -*-

from odoo.tests.common import users, TransactionCase

class TestControllerCase(TransactionCase):

    def setUp(self):
        super().setUp()

    def test_create_fill(self):
        data = {
            "trader_id": 1,
            "size": 0.001,
            "side": "buy",
            "price": 34343,        
        }
        res = requests.post("http://localhost:8069/cryptocurrency/create_fill", json=data)
        print(res.text)
        return

    def test_get_trader(self):
        data = {"trader_id": 1}
        res = requests.post("http://localhost:8069/cryptocurrency/get_trader", json=data)
        print(res.text)
        return

