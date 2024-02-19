# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'All in One Split Orders - Sale, Purchase, Picking/Delivery, Sale Split, Purchase Split, Delivery Split',
    'version': '15.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
        This Module add below functionality into odoo

        1.Create separate sale order for selected lines of selected sale order\n
        2.Create separate purchase order for selected lines of selected purchase order\n
        3.Create separate picking order for selected lines of selected picking\n
        
        Split Sale Order
Odoo split sale order
Split Quotation or Sale Order
Odoo Split Quotation or Sale Order
Easy to split quotation order
Odoo Easy to split quotation order
Easy to split sale order
Odoo easy to split sale order
Easy to extract quotation
Odoo Easy to extract quotation
Easy to extract sale order
Odoo easy to extract sale order
Split your sale order
Odoo split your sale order
Split sale ordrer odoo app
Split sale order odoo apps
Sale splitting
Odoo sale splitting
        
        odoo app allow Split Orders in sale, purchase, delivery, receipt, split sale order, split purchase order, split rfq, split delivery order, split quotation, sale split, purchase split, rfq split, quotation split, delivery split, split sale, order split

    """,
    'summary': 'odoo app allow Split Orders in sale, purchase, delivery, receipt, split sale order, split purchase order, split rfq, split delivery order, split quotation, sale split, purchase split, rfq split, quotation split, delivery split, split sale, order split',
    'depends': ['sale_management', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/dev_split_sale_view.xml',
        'wizard/split_sale_order_view.xml',
        'views/dev_split_purchase_view.xml',
        'wizard/split_purchase_order_view.xml',
        'views/dev_split_picking_view.xml',
        'wizard/split_picking_view.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':15.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
