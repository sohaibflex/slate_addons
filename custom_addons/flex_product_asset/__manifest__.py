# -*- coding: utf-8 -*-
{
    'name': 'Product Assets',
    'description': 'Link assets with products',
    'summary': '',
    'version': '14.0.1',
    'category': '',
    'author': 'Hossam Zaki - Flex-Ops',
    'website': 'https://flex-ops.com',
    'depends': [
        'product',
        'account_asset',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_asset.xml',
        'views/product_template.xml',
        'views/product_product.xml',

    ],
}
