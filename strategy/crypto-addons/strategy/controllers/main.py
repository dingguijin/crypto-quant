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

        strategy_id = data.get("strategy_id")
        if not strategy_id:
            _logger.error("no strategy_id %s" % data)
            return {}

        domain = [("id", "=", strategy_id)]
        strategy = request.env["mfbot.strategy"].sudo().search(domain)
        if not strategy:
            _logger.error("no strategy: %s" % data)
            return {}

        now = datetime.datetime.now()
        user_id = request.env.ref("base.user_admin")
        # user_id = strategy.user_id.id
        request.env["mfbot.fill"].with_user(user_id).create({
            "long_short": data.get("long_short"),
            "position_action": data.get("position_action"),
            "open_reason": data.get("open_reason"),
            "close_reason": data.get("close_reason"),
            "date": now,
            "strategy_id": strategy.id,
            "break_even_price": data.get("break_even_price"),
            "liquidation_price": data.get("liquidation_price"),
            "balance": data.get("balance"),
            "position": data.get("position"),
            "price": data.get("price"),
            "size": data.get("size"),
            "side": data.get("side").upper()})

        strategy.balance = data.get("balance")
        strategy.position = data.get("position")
        return {}

    @route('/cryptocurrency/update_pnl', type='json', methods=['POST'], auth='none', cors='*')
    def update_pnl(self, **kwargs):
        data = json.loads(request.httprequest.data)
        logging.info("data %s" % data)
        strategy_id = data.get("strategy_id")
        if not strategy_id:
            _logger.error("no strategy_id %s" % data)
            return {}
        
        domain = [("id", "=", strategy_id)]
        strategy = request.env["mfbot.strategy"].sudo().search(domain)
        if not strategy:
            _logger.error("no strategy: %s" % data)
            return {}

        balance = data.get("balance")
        position = data.get("position")

        now = datetime.datetime.now()
        pnl = balance.get("total_value") - strategy.balance
        user_id = request.env.ref("base.user_admin")
        # user_id = strategy.user_id.id
        request.env["mfbot.pnl"].with_user(user_id).create({
            "date": now,
            "pnl": pnl,
            "strategy_id": strategy.id,
            "price": position.get("price"),
            "size": position.get("size"),
            "side": position.get("side").upper(),
#            "break_even_price": position.get("break_even_price"),
            "liquidation_price": position.get("liquidation_price")})

        strategy.balance = balance.get("total_value")
        return {}
