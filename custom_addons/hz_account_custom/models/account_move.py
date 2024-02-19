# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            res = super(AccountMove, self)._compute_suitable_journal_ids()
            if self.move_type == 'entry':
                journal_type = ['general', 'bank', 'cash']
                company_id = m.company_id.id or self.env.company.id
                domain = [('company_id', '=', company_id), ('type', 'in', journal_type)]
                m.suitable_journal_ids = self.env['account.journal'].search(domain)
            return res

