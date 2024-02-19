from odoo import models, api, fields
from odoo import models, api, fields
import base64
from copy import copy
from locale import currency

import xlrd

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    bom_ids = fields.One2many('bom', 'product_template_id')
    excel_file = fields.Binary(string='Import Excel')
    amount_untaxed = fields.Monetary(string='Total Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    sub_total = fields.Float(related='bom_ids.sub_total')

    # def get_component(self):
    #     # active_ids = self.env.context.get('active_ids')
    #     # object_active_ids = self.env['product.template'].browse(active_ids)
    #     # for product in object_active_ids:
    #     #     bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', product.id)])
    #     #     component = []
    #     #     for product in bom_id.bom_line_ids.product_id:
    #     #         print(product)
    #             # component.append({
    #             #     'component_id':
    #             #     ,
    #             #     'quantity': bom_line.product_qty,
    #             # })
    #             # print(component)
    #     for product_template in self:
    #         bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', product_template.id)])
    #         component_list = []
    #         for component in bom_id.bom_line_ids:
    #             component_list.append({
    #                 'product_template_id': self.id,
    #                 'component_id': component.product_id.id,
    #                 'quantity': component.product_qty,
    #                 'cost': component.product_id.standard_price,
    #             })
    #         print(component_list)
    #         self.env['bom'].create(component_list)

    @api.depends('bom_ids.sub_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = 0.0
            for line in order.bom_ids:
                amount_untaxed += line.sub_total
            order.update({
                'amount_untaxed': amount_untaxed,
            })

    def _get_product_dict_key_import(self):
        return 'product_template_id'

    def import_from_excel(self):
        try:
            wb = xlrd.open_workbook(
                file_contents=base64.decodebytes(self.excel_file))
            sheet = wb.sheet_by_index(0)
            row_number = 0

            for row in range(sheet.nrows):
                if row == 0:
                    continue

                dic = {
                    self._get_product_dict_key_import(): self.id,
                    'component_id': self.env['component'].search([('name', 'ilike', sheet.cell(row, 0).value)]).id if sheet.cell(row, 0).value != '' else None,
                    'partner_id': self.env['res.partner'].search([('name', 'ilike', sheet.cell(row, 1).value)]).id if sheet.cell(row, 1).value != '' else None,
                    'quantity': sheet.cell(row, 2).value if sheet.cell(row, 2).value != '' else None,
                    'cost': sheet.cell(row, 3).value if sheet.cell(row, 3).value != '' else None,
                    'note': sheet.cell(row, 4).value if sheet.cell(row, 4).value != '' else None,
                }

                self.write({'bom_ids': [(0, 0, dic)]})
            self.excel_file = False;
        except Exception as e:
            raise UserError(
                _("Sorry, Your excel file does not match with our format " + str(e)))


class ProductProduct(models.Model):
    _inherit = "product.product"

    bom_ids = fields.One2many('bom', 'product_id')

    def _get_product_dict_key_import(self):
        return 'product_id'
