# -*- coding: utf-8 -*-
{
    'name'     : u'InfoSaône - Module Odoo kMyMoney',
    'version'  : u'0.1',
    'author'   : u'InfoSaône',
    'category' : u'InfoSaône',
    'description': u"""
InfoSaône - Module Odoo Module Odoo kMyMoney
===================================================
""",
    'maintainer' : u'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/is_kmymoney_view.xml',
    ],
    'installable': True,
    'application': True,
}
