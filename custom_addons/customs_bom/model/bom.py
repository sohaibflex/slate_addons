from odoo import models, api, fields
import base64
from copy import copy
from locale import currency

import xlrd

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime


class OpportunityType(models.Model):
    _name = 'bom'

    type = fields.Selection([('product', 'Product'), ('service', 'Service')], string='Type', default='product')

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        compute="_compute_product",
        store=True,
        readonly=False,
        ondelete="cascade",
    )
    product_template_id = fields.Many2one(
        comodel_name="product.template",
        compute="_compute_product_template",
        store=True,
        readonly=False,
        ondelete="cascade",
    )
    component_id = fields.Many2one('component', 'component')
    partner_id = fields.Many2one('res.partner', string='Partner')
    quantity = fields.Integer(string='Quantity', default=1)
    cost = fields.Float(string='Cost')
    note = fields.Text(string='Note')
    sub_total = fields.Float(string="SubTotal", compute="_compute_sub_total")

    @api.depends('cost', 'quantity')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.cost * record.quantity

    @api.depends("product_id")
    def _compute_product_template(self):
        for rec in self.filtered(lambda x: not x.product_template_id and x.product_id):
            rec.product_template_id = rec.product_id.product_tmpl_id

    @api.depends("product_template_id.product_variant_ids")
    def _compute_product(self):
        for rec in self.filtered(
            lambda x: not x.product_id and x.product_template_id.product_variant_ids
        ):
            rec.product_id = rec.product_template_id.product_variant_ids[0]


class Component(models.Model):
    _name = 'component'

    name = fields.Char('Name')