# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trade/exchange.py
#

from ftx_exchange import FtxExchange
from dydx_exchange import DydxExchange
from mxc_exchange import MxcExchange

import logging

def get_exchange(parser_args):    
    if parser_args.exchange == "mxc":
        return MxcGridExchange(parser_args.account_name)

    if parser_args.exchange == "dydx":
        return DydxExchange(parser_args.account_name)

    if parser_args.exchange == "ftx":
        return FtxExchange(account_name = parser_args.account_name, subaccount_name = parser_args.subaccount_name)

    logging.error("No exchange match %s" % parser_args.exchange)

    return None
