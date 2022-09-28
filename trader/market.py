# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trader/market.py
#

import logging

class Market():
    def __init__(self, name, size):
        self.name = name
        self.size = size
        return

def get_market(market_data):
    return Market(market_data.get("name"), market_data.get("size"))
