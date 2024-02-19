# -*- coding: utf-8 -*-
{
    'name': "Custom Sale Order Report",

    'summary': """
      Custom Sale Order Report""",

    'description': """
        Custom Sale Order Report
    """,

    'author': "Abdullah Almashaqbeh JO.",
    'website': "+962786664713",
    'version': '1.0',
    'license': 'LGPL-3',
    'currency': 'EUR',
    'depends': ['base', 'sale', 'sale_management'],

    'data': [
        'views/inherit_sale_order_report.xml',
    ],

}
