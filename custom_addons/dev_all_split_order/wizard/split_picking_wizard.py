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


class split_Transfer_confirm(models.TransientModel):
    """Split Transfer """
    _name = "split.transfer.confirm"

    def confirm(self):
        line_pool = self.env['stock.move']
        stock_pool = self.env['stock.picking']
        line_ids = self._context.get('active_ids')
        if line_ids:
            stock = line_pool.browse(line_ids[0]).picking_id
            if stock:
                vals = {
                    'partner_id': stock.partner_id.id or '',
                    'date': stock.date or '',
                    'picking_type_id': stock.picking_type_id.id or '',
                    'location_id': stock.location_id.id or '',
                    'location_dest_id': stock.location_dest_id.id or '',
                    'state': 'draft',
                }
                new_stock_id = stock_pool.create(vals)
                for line in line_pool.browse(line_ids):
                    line.write({'picking_id': new_stock_id.id})
                return {
                    'view_mode': 'form',
                    'res_id': new_stock_id.id,
                    'res_model': 'stock.picking',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                }

        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
