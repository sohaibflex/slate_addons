# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    asset_ids = fields.One2many('account.asset', 'product_tmpl_id', string='Assets')
    asset_count = fields.Integer(string='Assets', compute='_compute_asset_count')

    @api.depends('asset_ids')
    def _compute_asset_count(self):
        for product in self:
            product.asset_count = len(product.asset_ids)
