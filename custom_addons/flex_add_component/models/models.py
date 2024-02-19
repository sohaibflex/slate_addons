from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = 'stock.move'

    # bom_id = fields.Many2one('bom', 'BoM', compute='_compute_bom_id', store=True)
    product_component_id = fields.Many2many('component', string='Component', store=True,
                                            compute='_compute_product_component_id',
                                            readonly=False)

    @api.depends('product_id')
    def _compute_product_component_id(self):
        for record in self:
            if record.product_id.bom_ids:
                record.product_component_id = record.product_id.bom_ids.component_id
            else:
                record.product_component_id = False

    def action_compute_component(self):
        self._compute_product_component_id()


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_component_id = fields.Many2many('component', string='Component', store=True,
                                            compute='_compute_product_component_id',
                                            inverse='_inverse_product_component_id', readonly=False)

    @api.depends('move_id.product_component_id')
    def _compute_product_component_id(self):
        for record in self:
            if record.move_id.product_component_id:
                record.product_component_id = record.move_id.product_component_id
            else:
                record.product_component_id = False

    def _inverse_product_component_id(self):
        for record in self:
            record.move_id.product_component_id = record.product_component_id

    def action_compute_component(self):
        self._compute_product_component_id()
