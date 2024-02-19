{
    'name': 'Flex Add Component',
    'version': '14.0.0',
    'summary': 'Add Component',
    'description': 'Add Specific Component to Delivery Slip',
    'category': '',
    'author': 'Sohaib Alamleh||Flex-ops',
    'website': 'https://www.flex-ops.com',
    'license': '',
    'depends': ['base','sale_stock', 'mrp','customs_bom','stock_barcode'],
    'data': [
        'reports/delivery_slip_report.xml',
        'views/stock_move.xml',
        'views/stock_move_line.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
}