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
    
