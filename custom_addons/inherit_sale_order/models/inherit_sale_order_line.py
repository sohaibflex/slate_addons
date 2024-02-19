from odoo import fields, models, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    days = fields.Integer(string='Days', )
    daily_price = fields.Float(string='Daily Price')

    @api.onchange('product_uom', 'product_uom_qty')
    def _get_days_and_daily_price(self):
        if self.return_date and self.pickup_date:
            self.days = float((self.return_date - self.pickup_date).days)
        if self.days != 0:
            self.daily_price = float(self.price_unit) / float(self.days)


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    attention = fields.Char(string="Attention")
    project_name = fields.Char(string="Project Name",)

    def action_fix_day_and_daily_price(self):
        all_order_line = self.env['sale.order.line'].search([])
        for order_line in all_order_line:
            try:
                order_line.days = int(order_line.x_studio_days)
            except:
                pass
            order_line.daily_price = order_line.x_studio_daily_price



class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    project_name = fields.Char(string="Project Name",)


