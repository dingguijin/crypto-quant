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

