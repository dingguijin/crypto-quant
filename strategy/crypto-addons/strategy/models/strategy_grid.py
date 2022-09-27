# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models, api

class StrategyGrid(models.Model):
    _name = 'strategy.strategy_grid'

    _inherit = ['mail.thread',
                'mail.activity.mixin',
                'trade.strategy']

    _rec_name = "id"

    strategy = fields.Selection(selection_add=[('GRID', 'GRID')])

    grid_gap = fields.Float('Grid gap', track_visibility='onchange')
    grid_size = fields.Float('Grid size', track_visibility='onchange')
    
