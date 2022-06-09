from odoo import models, _

class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    def post(self):
        res = super(AccountPaymentGroup, self).post()
        self.imputed_payments()
        return res
    
    def imputed_payments(self):
        if len(self.matched_move_line_ids) != 0:
            for line in self.matched_move_line_ids:
                if line.invoice_id.origin != '':
                    so = self.env['sale.order'].search([('name', '=', line.invoice_id.origin)], limit=1)
                    vals = {
                        "name": _("Payment"),
                        "payment_id": self.id,
                        "amount_imputed": self.amount_to_impute,
                        "order_id": so.id,
                        "state": "imputed"
                    }
                    self.env["sale.order.advancement"].create(vals)

