# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trader/exchange.py
#

from ftx_exchange import FtxExchange
from dydx_exchange import DydxExchange
from mxc_exchange import MxcExchange

import logging

def get_exchange(name):    
    if name == "mxc":
        return MxcGridExchange()

    if name == "dydx":
        return DydxExchange()

    if name == "ftx":
        return FtxExchange()

    logging.error("No exchange match %s" % name)
    return None
