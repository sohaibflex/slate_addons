import base64
import binascii
import csv
import tempfile
from copy import copy
from locale import currency
import io

import xlrd
from xlrd import xlsx

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        print(vals)
        return super(SaleOrderLine, self).create(vals)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_pickup(self):
        pass

    def action_sale_order_lines(self):
        self.ensure_one()
        return {
            'name': f"{self.name} Lines",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'tree',
            'target': 'current',
            'view_id': self.env.ref('flex_import_excel.sale_order_line_tree_editable').id,
            'domain': [('order_id', 'in', self.ids)],
            'context': {'default_order_id': self.id,
                        'default_state': 'draft',
                        'create': self.state in ['draft', 'sent'],
                        'edit': self.state in ['draft', 'sent'],
                        'delete': self.state in ['draft', 'sent'],
                        },
        }
