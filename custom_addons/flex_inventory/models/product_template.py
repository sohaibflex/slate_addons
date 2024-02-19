# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    date = fields.Date(string="Date", default=fields.Date.today())
    account_cost = fields.Float(string="Account Cost")


class ProductProduct(models.Model):
    _inherit = "product.product"

    date = fields.Date(string="Date", default=fields.Date.today())
    account_cost = fields.Float(string="Account Cost")
    qty_variant = fields.Float(string='Quantity')
