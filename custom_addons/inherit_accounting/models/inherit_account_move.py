from odoo import fields, models, api, _

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    bank_details = fields.Text(string="Bank Details", Default="")


