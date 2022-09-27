# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models, api

class Strategy(models.Model):
    _name = 'strategy.strategy'

    _inherit = ['mail.thread',
                'mail.activity.mixin']

    _rec_name = "id"

    strategy = fields.Selection([], string='Strategy', help='Select a strategy')
    
    able_to_modify = fields.Boolean(string='Able to modify', compute='_compute_able_to_modify')

    def _compute_able_to_modify(self):
        for record in self:
            record.able_to_modify = self.env.user.has_group('strategy.group_strategy_manager')
