import json
import logging
import datetime

from odoo import exceptions, _
from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)

class MainController(Controller):

    @route('/cryptocurrency/create_fill', type='json', methods=['POST'], auth='none', cors='*')
    def create_fill(self, **kwargs):
        data = json.loads(request.httprequest.data)
        logging.info("data %s" % data)

        trader_id = data.get("trader_id")
        if not trader_id:
            _logger.error("no trader_id %s" % data)
            return {}

        domain = [("id", "=", strategy_id)]
        trader = request.env["strategy.trader"].sudo().search(domain)
        if not trader:
            _logger.error("no trader: %s" % data)
            return {}

        now = datetime.datetime.now()
        user_id = request.env.ref("base.user_admin")
        # user_id = strategy.user_id.id
        request.env["strategy.fill"].with_user(user_id).create({
            "long_short": data.get("long_short"),
            "position_action": data.get("position_action"),
            "open_reason": data.get("open_reason"),
            "close_reason": data.get("close_reason"),
            "date": now,
            "trader_id": trader.id,
            "break_even_price": data.get("break_even_price"),
            "liquidation_price": data.get("liquidation_price"),
            "balance": data.get("balance"),
            "position": data.get("position"),
            "price": data.get("price"),
            "size": data.get("size"),
            "side": data.get("side").upper()})
        return {}

    @route('/cryptocurrency/get_trader', type='json', methods=['POST'], auth='none', cors='*')
    def update_pnl(self, **kwargs):
        data = json.loads(request.httprequest.data)
        logging.info("data %s" % data)
        trader_id = data.get("trader_id")
        if not trader_id:
            _logger.error("no trader_id %s" % data)
            return {}
        
        domain = [("id", "=", trader_id)]
        trader = request.env["strategy.trader"].sudo().search(domain)
        if not trader:
            _logger.error("no trader: %s" % data)
            return {}

        now = datetime.datetime.now()
        trader.write({"last_run_time": now})
        _logger.info(dict(trader[0]))
        return dict(trader[0])
