import time
import datetime
import logging
import requests

from trade_side import TradeSide
from trade_type import TradeType

from strategy import Strategy

class GridStrategy(Strategy):
    def init_with_strategy_data(self, strategy_data):
        super().init_with_strategy_data(strategy_data)
                
        self.grid_exchange = self.trader.exchange

        self.grid_gap = self.strategy_data.get("grid_gap")
        self.base_grid_gap = self.strategy_data.get("grid_gap")        
        self.grid_size = self.strategy_data.get("grid_size")

        self.placed_orders = []
        self.position_sizes = []
        return

    def strategy_loop_once(self):
        """ Isolate "get placed orders" and "get fills" logic
        
        get placed orders == 2, 1, 0:
        if 0 get current price, place two orders
        if 1 cancel all orders
        if 2 get current price, legal continue, illegal cancel all orders
        append placed orders id placed_orders array

        get fills always 4:
        if fills is None, continue
        if fills not None and:
        if fills in in placed_orders, remove all orders before fills in placed_orders, log into db
        if fills not in placed_orders, continue
        """
        
        return

    def get_next_sell_price(self, position_price):
        return position_price*(1+self.grid_gap_ratio)

    def get_next_buy_price(self, position_price):
        return position_price*(1-self.grid_gap_ratio)

    def place_grid_sell_order(self, price, order_type=TradeType.LIMIT):
        trade_side = self.grid_exchange.convert_side_for_exchange(TradeSide.SELL)
        placed_order = None
        if order_type == TradeType.LIMIT:
            placed_order = self.grid_exchange.place_limit_order(self.market, self.size, trade_side, price)
        if order_type == TradeType.MARKET:
            placed_order = self.grid_exchange.place_market_order(self.market, self.size, trade_side, price)
        if placed_order != None:
            self.placed_orders.append(placed_order)
        return placed_order

    def place_grid_buy_order(self, price, order_type=TradeType.LIMIT):
        trade_side = self.grid_exchange.convert_side_for_exchange(TradeSide.BUY)
        placed_order = None
        if order_type == TradeType.LIMIT:
            placed_order = self.grid_exchange.place_limit_order(self.market, self.size, trade_side, price)
        if order_type == TradeType.MARKET:
            placed_order = self.grid_exchange.place_market_order(self.market, self.size, trade_side, price)
        if placed_order != None:
            self.placed_orders.append(placed_order)
        return placed_order

    def _find_lastest_fill_orders(self, fills):
        order_ids = set()
        for fill in fills:
            order_ids.add(fill.get("order_id"))
        filled_orders = list(filter(lambda x: x.get("order_id") in order_ids, self.placed_orders))
        unfilled_orders = list(filter(lambda x: x.get("order_id") not in order_ids, self.placed_orders))
        return filled_orders, unfilled_orders
    
    def on_fills_update(self, fills):
        _filled_orders, _unfilled_orders = self._find_lastest_fill_orders(fills)
        if not _filled_orders:
            return None
        
        logging.info("filled_orders %s" % _filled_orders)

        cancel_ids = list(map(lambda x: x.get("order_id"), _unfilled_orders))
        if cancel_ids:
            self.cancel_unfilled_orders(cancel_ids)

        self.create_odoo_fill(_filled_orders[0])
        
        # use latest order price, but not the grid price
        # so that we can set very small step 
        # _last_price = self.grid_exchange.get_last_price(self.market)
        # _last_price = _last_price.get("price")

        # logging.info("get last price: %s" % _last_price)
        _last_price = _filled_orders[0].get("price")
        # reinit placed orders

        self.placed_orders = []
        self.replace_grid_orders(_last_price)

        return self.placed_orders

    def cancel_unfilled_orders(self, cancel_ids):
        if not cancel_ids:
            return
        logging.info("cancel all unfilled orders: %s" % cancel_ids)
        cancelled_ids = self.grid_exchange.cancel_orders(cancel_ids)
        return cancelled_ids

    def replace_grid_orders(self, latest_price):
        self.sleep_seconds = 0
        
        buy_price = self.get_next_buy_price(latest_price)
        sell_price = self.get_next_sell_price(latest_price)

        logging.info("get filled: %s buy: %s, sell: %s" % (latest_price, buy_price, sell_price))
        # FIXME: if next price overflow the pricelist, dangerous!!!
        if buy_price != None:
            self.place_grid_buy_order(buy_price)
        if sell_price != None:
            self.place_grid_sell_order(sell_price)
        return
        
    def sleep_strategy(self, seconds):
        time.sleep(seconds)
        self.sleep_seconds = self.sleep_seconds + seconds
        self.grid_step_ratio_sleep = self.grid_step_ratio_sleep + seconds
        self.update_odoo_pnl_sleep = self.update_odoo_pnl_sleep + seconds
        return self.sleep_seconds

    def check_wrong_orders(self):
        # reset sleep seconds when place order
        if self.sleep_seconds < 5.0:
            return
        self.sleep_seconds = 0
        
        last_trade = self.grid_exchange.get_last_trade(self.market)
        if not last_trade:
            logging.error("no last trade")
            return
        last_price = float(last_trade.get("price"))
        
        open_orders = self.grid_exchange.get_open_orders(self.market) or []
        prices = []
        if len(open_orders) == 2:
            prices.append(float(open_orders[0].get("price")))
            prices.append(float(open_orders[1].get("price")))
            if last_price > min(prices) and last_price < max(prices):
                logging.info("orders is right 2, keep waiting %s" % self.sleep_seconds)
                return

        logging.error("open orders != 2 %s, waiting: %s" % (open_orders, self.sleep_seconds))
        if open_orders:
            cancel_ids = list(map(lambda x: x.get("order_id"), open_orders))
            self.grid_exchange.cancel_orders(cancel_ids)
        # reinit
        self.placed_orders = []
        self.replace_grid_orders(last_trade.get("price"))
        return
    
    def caculate_grid_step_ratio(self):
        if True:
            self.grid_gap_ratio = self.base_grid_gap_ratio
            return

        # comments other code
        if self.grid_step_ratio_sleep < 60.0:
            return
        self.grid_step_ratio_sleep = 0

        positions = self.grid_exchange.get_open_positions(self.market)
        if not positions:
            return

        logging.info("positions ... %s" % positions)
        positions = list(filter(lambda x: x.get("size") > 0.0, positions))
        if not positions:
            return

        position = positions[0]
        logging.info("position ... %s" % position)
        # if position.get("pnl") > 0.0:
        #     return

        account_balance = self.grid_exchange.get_account_balance()
        if not account_balance:
            logging.info("no account balance")
            return

        total_value = account_balance.get("total_value")
        total_position = account_balance.get("total_position")

        logging.info("account balance: %s" % account_balance)
        
        # less than 80%
        if total_value * 0.80 >= total_position:
            self.grid_gap_ratio = self.base_grid_gap_ratio
            logging.info("grid gap ratio 1x %s" % self.grid_gap_ratio)
            return

        # between 80% - 100%
        if total_value * 0.80 < total_position and total_value >= total_position:
            self.grid_gap_ratio = 1.5*self.base_grid_gap_ratio
            logging.info("grid gap ratio 2x %s" % self.grid_gap_ratio)
            return

        # between 100% - 200%
        if total_value < total_position and total_value*2.0 >= total_position:
            self.grid_gap_ratio = 2.0*self.base_grid_gap_ratio
            logging.info("grid gap ratio 4x %s" % self.grid_gap_ratio)
            return

        # larger than 200%
        if total_value*2.0 < total_position:
            self.grid_gap_ratio = 3.0*self.base_grid_gap_ratio
            logging.info("grid gap ratio 8x %s" % self.grid_gap_ratio)
            return

        logging.info("keep grid gap ratio ?x %s" % self.grid_gap_ratio)
        return

    def create_odoo_fill(self, fill):
        account_balance = self.grid_exchange.get_account_balance()
        if not account_balance:
            logging.info("no account balance")
            return

        balance = account_balance.get("total_value")

        positions = self.grid_exchange.get_open_positions(self.market)
        position = {}
        if positions:
            position = positions[0]

        logging.info("fill send: %s" % fill)

        data = {
            "strategy_id": self.strategy_id,
            "size": fill.get("size"),
            "price": fill.get("price"),
            "side": fill.get("side"),
            "balance": balance,
            "position": position.get("net_size"),
            "break_even_price": position.get("break_even_price"),
            "liquidation_price": position.get("liquidation_price")
        }
        res = requests.post("http://localhost:8069/cryptocurrency/create_fill", json=data)
        logging.info("res %s for %s" % (res.text, data))
