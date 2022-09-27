# -*- coding: utf-8 -*-


{
    'name': 'Strategy',
    'category': 'Cryptocurrency',
    'summary': 'Crypto Quant strategy configuration',
    'version': '1.0',
    'description': """
        This module provides the multiple strategies for quantitative trading.
        """,
    'depends': [ 'web', "mail" ],
    'data': [
        'security/strategy_security.xml',
        'security/ir.model.access.csv',

        'views/strategy_views.xml',
        'views/fill_views.xml',

        'views/fill_actions.xml',
        'views/strategy_actions.xml',

        'views/menu.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'strategy/static/src/xml/**/*',
        ],
        'web.assets_backend': [
            'strategy/static/src/**/*',
        ],
        'web.tests_assets': [
            'strategy/static/tests/helpers/**/*',
        ],
        'web.qunit_mobile_suite_tests': [
            'strategy/static/tests/*_tests.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'GPL-3',
}
