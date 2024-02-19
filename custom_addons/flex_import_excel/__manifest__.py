# -*- coding: utf-8 -*-
{
    'name': 'Flex Import Excel ',
    'version': '14.0.1',
    'description': '',
    'summary': '',
    'author': "Ahmad Hasan - Flex-Ops",
    'website': "https://flex-ops.com",
    'depends': ['base', 'sale', 'sale_renting', 'inherit_sale_order'],

    'data': [
        'security/ir.model.access.csv',
        'views/import_excel_view.xml',

    ],

    'installable': True,
    'auto_install': False,
}
