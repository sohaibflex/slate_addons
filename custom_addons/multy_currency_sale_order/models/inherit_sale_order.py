# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class KsGlobalDiscountSales(models.Model):
    _inherit = "sale.order"

    show_amount_currency = fields.Boolean('Show')
    amount_currency = fields.Char('Amount In Diff. Currency')