# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models, api

class Exchange(models.Model):
    _name = 'strategy.exchange'

    _inherit = ['mail.thread',
                'mail.activity.mixin']

    _rec_name = "id"

    symbol = fields.Char(string='Symbol', required=True)
    name = fields.Char(string='Name', required=True)

    maker_fee = fields.float(string='Maker fee')
    taker_fee = fields.float(string='Taker fee')
    
    desc = fields.Char(string='Description')

    able_to_modify = fields.Boolean(string='Able to modify', compute='_compute_able_to_modify')

    def _compute_able_to_modify(self):
        for record in self:
            record.able_to_modify = self.env.user.has_group('strategy.group_strategy_manager')
