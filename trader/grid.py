# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trade/grid.py
#

import os
import sys
import logging
import argparse

import math
import time
import datetime
import itertools
import argparse

from enum import Enum
from dotenv import load_dotenv
load_dotenv()

import pprint

from grid_strategy import GridStrategy
from exchange import get_exchange

def _init_grid_strategy(parser_args, grid_exchange, init_price):
    step_ratio = parser_args.step_ratio
    strategy_id = parser_args.strategy_id
    market = parser_args.market
    size = parser_args.size
    return GridStrategy(grid_exchange, market, size, init_price, step_ratio, strategy_id)

def _start_grid_loop(parser_args):

    grid_exchange = get_exchange(parser_args)
    if not grid_exchange:
        logging.error("no exchange for args: %s" % sys.argv)
        exit(-1)

    market = parser_args.market
    last_trade = grid_exchange.get_last_trade(market)

    if not last_trade:
        logging.error("no last trade")
        exit(-1)

    init_price = last_trade.get("price")
    grid_strategy = _init_grid_strategy(parser_args, grid_exchange, init_price)

    grid_strategy.open_initial_position()

    while True:
        grid_strategy.sleep_strategy(0.5)
        grid_strategy.caculate_grid_step_ratio()
        
        fills = grid_exchange.get_fills(market, limit=4)
        if not fills:
            # should not be here, since init with open/close orders
            grid_strategy.check_wrong_orders()
            continue
        
        if grid_strategy.on_fills_update(fills):
            continue

        grid_strategy.check_wrong_orders()
        # grid_strategy.update_odoo_pnl()
        
def _init_grid_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange", type=str, required=True)
    parser.add_argument("--market", type=str, required=True)
    parser.add_argument("--size", type=float, required=True)
    parser.add_argument("--step_ratio", type=float, required=True)
    parser.add_argument("--account_name", type=str, required=False)
    parser.add_argument("--subaccount_name", type=str, required=False)
    parser.add_argument("--strategy_id", type=int, required=False)
    return parser.parse_args()

if __name__ == "__main__":

    parser_args = _init_grid_arguments()

    _root_dir = os.path.join(os.path.dirname(__file__), "../../")
    sys.path.append(os.path.abspath(_root_dir))

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
        
    _start_grid_loop(parser_args)
