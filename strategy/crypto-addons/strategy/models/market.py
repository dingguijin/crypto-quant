# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 ~
# Guijin Ding, dingguijin@gmail.com
#
# All rights reserved
#

from odoo import fields, models, api

class Market(models.Model):
    _name = 'strategy.market'

    _inherit = ['mail.thread',
                'mail.activity.mixin']

    _rec_name = "id"

    symbol = fields.Char(string='Symbol', required=True)
    name = fields.Char(string='Name')
    desc = fields.Char(string='Description')
    
