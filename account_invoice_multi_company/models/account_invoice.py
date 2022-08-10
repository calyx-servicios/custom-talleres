from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        invoice.account_id = invoice.partner_id.with_context(force_company=invoice.company_id.id).property_account_receivable_id.id
        return invoice