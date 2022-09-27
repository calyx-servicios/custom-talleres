from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit="account.invoice"


    account_id = fields.Many2one("account.account", compute="_get_account")


    @api.depends("partner_id")
    def _get_account(self):
        for record in self:
            if record.partner_id.supplier == True:
                record.update({"account_id": record.partner_id.property_account_payable_id})
