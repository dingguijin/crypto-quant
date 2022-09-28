# -*- coding: utf-8 -*-
#
# Copyright (C) from 2022.
# Guijin Ding, dingguijin@gmail.com.
# All rights are reserved.
#
# trade/main.py
#

import os
import sys
import time
import logging
import argparse
        
def _init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trader_id", type=int, required=True)
    return parser.parse_args()

def _register_signal():
    # TODO: register signal to stop the process
    return

def _main():
    odoo_client = OdooClient()
    trader = Trader(odoo_client)

    trader_data = trader.get_trader(parser_args.trader_id)
    if not trader_data:
        logging.error("No trader: [%s]" % parser_args.trader_id)
        return
    trader.trader_data = trader_data
    
    logging.info("Start trader: [%s]" % parser_args.trader_id)
    exchange = trader.init_exchange(trader_data)
    if not exchange:
        return
    trader.exchange = exchange
    
    market_data = trader.init_market(trader_data)
    if not market_data:
        return
    trader.market_data = market_data

    strategy = trader.init_strategy(trader_data)
    if not strategy:
        return
    trader.strategy = strategy

    trader.loop()
    return

if __name__ == "__main__":
    parser_args = _init_arguments()
    _root_dir = os.path.join(os.path.dirname(__file__), "../../")
    sys.path.append(os.path.abspath(_root_dir))

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
              
    _register_signal()
    _main()
    logging.error("Unexpect exit trader: [%s]" % parser_args.trader_id)
