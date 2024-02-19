# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, models, _


class split_order_confirm(models.TransientModel):
    _name = "split.so.order.confirm"

    def confirm(self):
        line_pool = self.env['sale.order.line']
        line_ids = self._context.get('active_ids')
        if line_ids:
            sale = line_pool.browse(line_ids[0]).order_id
            print("--------sale---------",sale)
            if sale:
                vals = {
                    'partner_id': sale.partner_id.id or '',
                    'date_order': sale.date_order or '',
                    'warehouse_id': sale.warehouse_id.id or '',
                    'pricelist_id': sale.pricelist_id.id or '',
                    'state': 'draft',
                    'origin': sale.name,
                }
                new_sale_id = self.env['sale.order'].create(vals)
                print("-----new_sale_id-------",new_sale_id)
            for line in line_pool.browse(line_ids):
                line.write({'order_id': new_sale_id.id})
            return {
                'view_mode': 'form',
                'res_id': new_sale_id.id,
                'res_model': 'sale.order',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': self._context,
            }

        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
