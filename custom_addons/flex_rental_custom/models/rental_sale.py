from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    receipt_count = fields.Integer(compute='_compute_receipt_count')
    delivery_count_new = fields.Integer(compute='_compute_delivery_count_new')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.create_delivery_order_and_moves()
        return res

    def action_show_delivery(self):
        self.action_view_delivery()
        return {
            'name': _('Delivery Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('sale_id', '=', self.id), ('picking_type_id.code', '=', 'outgoing')],
        }

    def create_delivery_order_and_moves(self):
        DeliveryOrder = self.env['stock.picking']
        StockMove = self.env['stock.move']

        for order in self:
            if order.picking_ids:
                continue
            # continue
            delivery_vals = {
                'partner_id': order.partner_shipping_id.id,
                'scheduled_date': fields.Datetime.now(),
                'picking_type_id': order.warehouse_id.out_type_id.id,
                'origin': order.name,
                'location_id': order.warehouse_id.lot_stock_id.id,
                'location_dest_id': order.partner_shipping_id.property_stock_customer.id,
                'state': 'assigned',
                'sale_id': order.id,

            }

            delivery_order = DeliveryOrder.create(delivery_vals)

            for line in order.order_line:
                # if not  note or section
                if line.product_id:
                    move_vals = {
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'picking_id': delivery_order.id,
                        'location_id': order.warehouse_id.lot_stock_id.id,
                        'location_dest_id': order.partner_shipping_id.property_stock_customer.id,
                        # 'state': 'assigned',
                        'sale_line_id': line.id,

                    }
                    StockMove.create(move_vals)

            order.write({'picking_ids': [(4, delivery_order.id)]})

        return True

    def create_receipt_order_and_moves(self):
        # for x in self:
        DeliveryOrder = self.env['stock.picking']
        StockMove = self.env['stock.move']

        for order in self:

            receipt_vals = {
                'partner_id': order.partner_shipping_id.id,
                'scheduled_date': fields.Datetime.now(),
                'picking_type_id': order.warehouse_id.in_type_id.id,
                'origin': order.name,
                'location_id': order.partner_shipping_id.property_stock_customer.id,
                'location_dest_id': order.warehouse_id.lot_stock_id.id,
                'state': 'draft',
            }

            receipt_order = DeliveryOrder.create(receipt_vals)

            for line in order.order_line:
                if line.product_id:
                    move_vals = {
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'picking_id': receipt_order.id,
                        'location_id': order.partner_shipping_id.property_stock_customer.id,
                        'location_dest_id': order.warehouse_id.lot_stock_id.id,
                        'state': 'draft',
                    }
                    StockMove.create(move_vals)

            order.write({'picking_ids': [(4, receipt_order.id)]})
        return True

    def action_show_receipt(self):
        # self.ensure_one()
        # # return receipt order when click on validate button in returned wizard
        # if self.env.context.get('return_picking_id'):
        #     return self.env['stock.picking'].browse(self.env.context.get('return_picking_id')).action_show_receipt()
        # self.action_show_receipt()
        return {
            'name': _('Receipt Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('sale_id', '=', self.id), ('picking_type_id.code', '=', 'incoming')],
        }

    def _compute_receipt_count(self):
        for order in self:
            order.receipt_count = len(order.picking_ids.filtered(lambda x: x.picking_type_id.code == 'incoming'))

    def _compute_delivery_count_new(self):
        for order in self:
            order.delivery_count_new = len(order.picking_ids.filtered(lambda x: x.picking_type_id.code == 'outgoing'))


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking
            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(
                float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line
                in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(
                        lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(
                    products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(
                    pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _(
                    '\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(
                    pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (
                    ', '.join(pickings_without_lots.mapped('name')),
                    ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())

        # # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res
        if self.env.context.get('picking_ids_not_to_backorder'):
            pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
            pickings_to_backorder = self - pickings_not_to_backorder
        else:
            pickings_not_to_backorder = self.env['stock.picking']
            pickings_to_backorder = self
        if self.picking_type_id.code == 'outgoing':
            for line in self.move_lines:
                if line.sale_line_id:
                    line.sale_line_id.qty_delivered = line.sale_line_id.qty_delivered + line.product_uom_qty
        pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
        pickings_to_backorder.with_context(cancel_backorder=False)._action_done()
        self.write({'state': 'done'})
        return True
        # change state to done

        # else:
        # apply detailed operation for returned products

        # else:
        #     for line in self.move_lines:
        #         if line.sale_line_id:
        #             line.sale_line_id.qty_returned = line.sale_line_id.qty_returned + line.product_uom_qty


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def create_returns(self):
        for wizard in self:
            new_picking_id, pick_type_id = wizard._create_returns()
            if new_picking_id:
                if self.env.context.get('active_model') == 'stock.picking':
                    sale_id = self.env['stock.picking'].browse(self.env.context.get('active_id')).sale_id
                    self.env['stock.picking'].browse(new_picking_id).sale_id = sale_id.id
        # Override the context to disable all the potential filters that could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'default_partner_id': self.picking_id.partner_id.id,
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_planning_issues': False,
            'search_default_available': False,
        })
        for line in self.product_return_moves:
            if line.move_id.sale_line_id:
                line.move_id.sale_line_id.qty_returned = line.move_id.sale_line_id.qty_returned + line.quantity
            if line.move_id.sale_line_id.qty_delivered == 0:
                line.move_id.sale_line_id.qty_delivered = line.move_id.sale_line_id.qty_delivered + line.quantity

        return {
            'name': _('Returned Picking'),
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class RentalOrderWizard(models.TransientModel):
    _inherit = 'rental.order.wizard'

    def apply(self):
        for wizard in self:
            msg = wizard.rental_wizard_line_ids._apply()
            if msg:
                for key, value in wizard._fields['status']._description_selection(wizard.env):
                    if key == wizard.status:
                        translated_status = value
                        break

                header = "<b>" + translated_status + "</b>:<ul>"
                msg = header + msg + "</ul>"
                wizard.order_id.message_post(body=msg)

        # create receipt order
        if self.status == 'return':
            self.order_id.create_receipt_order_and_moves()

        return  # {'type': 'ir.actions.act_window_close'}
