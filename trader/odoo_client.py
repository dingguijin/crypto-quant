# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trader/odoo_client.py
#

import os
import sys
import logging
import requests
import singleton

class OdooClient(metaclass=singleton.Singleton):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        return

    def create_fill(self, fill):
        res = requests.post("http://%s:%s/cryptocurrency/create_fill" % (self.host, self.port),
                            json=fill)
        logging.info("create_fill, res %s for %s" % (res.text, fill))
        return res

    def get_trader(self, trader_id):
        data = {"trader_id": trader_id}
        res = requests.post("http://%s:%s/cryptocurrency/get_trader" % (self.host, self.port),
                            json=data)
        logging.info("get_trader res %s for %s" % (res.text, data))
        return res

    def update_trader_pid(self, trader_id, pid):
        data = {"trader_id": trader_id, "pid": pid}
        res = requests.post("http://%s:%s/cryptocurrency/update_trader_pid" % (self.host, self.port),
                            json=data)
        logging.info("update_trader_pid res %s for %s" % (res.text, data))
        return
