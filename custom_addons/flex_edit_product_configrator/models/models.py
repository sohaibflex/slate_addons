from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    display_type = fields.Selection([
        ('radio', 'Radio'),
        ('select', 'Select'),
        ('color', 'Color'),
        ('checkbox', 'Checkbox')], default='radio', required=True,
        help="The display type used in the Product Configurator.")

    @api.constrains('display_type', 'create_variant')
    def _check_checkbox_no_variant(self):
        for attribute in self:
            if attribute.display_type == 'checkbox' and attribute.create_variant != 'no_variant':
                raise ValidationError("Multi-checkbox display type is not compatible with the creation of variants")
