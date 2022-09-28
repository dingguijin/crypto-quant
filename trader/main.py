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
        
def _init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trader_id", type=int, required=True)
    return parser.parse_args()


if __name__ == "__main__":

    parser_args = _init_arguments()

    _root_dir = os.path.join(os.path.dirname(__file__), "../../")
    sys.path.append(os.path.abspath(_root_dir))

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    trader = Trader().get_trader(parser_args.trader_id)
    if not trader:
        logging.error("No trader: %s" % parser_args.trader_id)
        exit(-1)
