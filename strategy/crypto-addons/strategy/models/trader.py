# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models, api

class Trader(models.Model):
    _name = 'strategy.trader'

    _inherit = ['mail.thread',
                'mail.activity.mixin']

    _rec_name = "id"

    strategy_id = fields.Many2one('strategy.strategy', string='Strategy')
    exchange_id = fields.Many2one(trade.exchange, string='Exchange', required=True, help='Select a exchange')

    market_id = fields.Many2one(trade.market, string='Market', required=True, help='Select a coin')

    invest = fields.Float('invest', track_visibility='onchange')
    
    balance = fields.Float('balance', readonly=True)
    pnl = fields.Float('Profit and Loss', compute='_compute_pnl', readonly=True)
    position = fields.Float('Position', readonly=True)
    
    user_id = fields.Many2one('res.users', string='User')
    subaccount = fields.Char('Exchage subaccount')

    fill_lines = fields.One2many('trade.fill', 'trader_id', string='Fill lines')

    misc = fields.Text('Misc')

    start_date = fields.Datetime('Start Time', track_visibility='onchange')

    able_to_modify = fields.Boolean('Able to modify', compute='_compute_able_to_modify')
    
    @api.model
    def create(self, vals):
        if vals.get("invest"):
            vals["balance"] = vals.get("invest")
        return super().create(vals)

    @api.depends('invest', 'balance')
    def _compute_pnl(self):
        for record in self:
            if record.balance == 0.0:
                record.pnl = 0.0
            else:
                record.pnl = record.balance - record.invest

    def _compute_able_to_modify(self):
        for record in self:
            record.able_to_modify = self.env.user.has_group('trade.group_trade_manager')
