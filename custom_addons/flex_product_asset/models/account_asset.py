# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountAsset(models.Model):
    _inherit = "account.asset"

    product_tmpl_id = fields.Many2one('product.template', string='Product Template', ondelete='restrict')
    product_id = fields.Many2one('product.product', string='Product Variant', ondelete='restrict')
    product_qty = fields.Float(string='Product Qty')
