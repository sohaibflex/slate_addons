# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, _
from datetime import datetime

class split_po_order_confirm(models.TransientModel):
    _name = "split.po.order.confirm"

    def confirm_purchase(self):
        line_pool = self.env['purchase.order.line']
        purchase_pool = self.env['purchase.order']
        line_ids = self._context.get('active_ids')
        if line_ids:
            purchase = line_pool.browse(line_ids[0]).order_id
            if purchase:
                vals = {
                    'partner_id': purchase.partner_id.id or '',
                    'date_order': purchase.date_order or '',
                    'company_id': purchase.company_id.id or '',
                    'picking_type_id': purchase.picking_type_id.id or '',
                    'state': 'draft',
                    'origin': purchase.origin,
                }
                if purchase.date_planned:
                    date = datetime.strptime(str(purchase.date_planned),
                                             '%Y-%m-%d %H:%M:%S')
                    vals.update({'date_planned': date})
                new_purchase_id = purchase_pool.create(vals)
            for line in line_pool.browse(line_ids):
                line.write({'order_id': new_purchase_id.id})
            return {
                'view_mode': 'form',
                'res_id': new_purchase_id.id,
                'res_model': 'purchase.order',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': self._context,
            }

        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
