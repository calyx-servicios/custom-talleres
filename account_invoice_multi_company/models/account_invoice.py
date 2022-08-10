from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        res.account_id = res.partner_id.with_context(force_company=1).property_account_receivable_id.id
        return res