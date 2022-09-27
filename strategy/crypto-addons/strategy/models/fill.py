# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models

class Fill(models.Model):
    _name = 'strategy.fill'
    _rec_name = "id"
    _order = "date desc"

    _inherit = ['mail.thread',
                'mail.activity.mixin']

    trader_id = fields.Many2one('strategy.trader', 'Trader')
    strategy_id = fields.Many2one('strategy.strategy', 'Strategy')
    
    user_id = fields.Many2one('res.users', related='trader_id.user_id')
    market = fields.Many2one('strategy.market', related='strategy_id.market')
    
    side = fields.Selection([
        ('BUY', 'BUY'),
        ('SELL', 'SELL')], 
        string='Direction', required=True)

    size = fields.Float('size', readonly=True)
    price = fields.Float('price', readonly=True)

    pnl = fields.Float('Profit and loss', readonly=True)
    balance = fields.Float('Balance', readonly=True)
    position = fields.Float('Position', readonly=True)
    
    break_even_price = fields.Float('Break even price', readonly=True)
    liquidation_price = fields.Float('Liquidation price', readonly=True)

    fill_time = fields.Datetime('Time', readonly=True)

    position_action = fields.Selection([
        ('OPEN', 'OPEN'),
        ('CLOSE', 'CLOSE')], 
        string='Action', required=False)

    close_reason = fields.Selection([
        ('STOP_LOSS', 'STOP_LOSS'),
        ('STOP_PROFIT', 'STOP_PROFIT'),
        ('MANUAL', 'MANUAL')], string='Close Reason', required=False)

    able_to_modify = fields.Boolean(string='Able to modify', compute='_compute_able_to_modify')

    def _compute_able_to_modify(self):
        for record in self:
            record.able_to_modify = self.env.user.has_group('strategy.group_strategy_manager')
