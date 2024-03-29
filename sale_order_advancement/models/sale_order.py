# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    advancement_line_ids = fields.One2many(
        "sale.order.advancement", "order_id", string="Advancement Lines"
    )
    calcule_amount_residual = fields.Monetary(
        string="Amount Residual",
        readonly=True,
        compute="_compute_amount_residual",
    )
    calcule_amount_imputed = fields.Monetary(
        string="Payment", readonly=True, compute="_compute_amount_residual",
    )

    @api.multi
    def create_payment(self):
        return{
            "name": "Crear Recibo",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.payment.group",
            "view_id": False,
            "target": "new",
        }

    @api.depends(
        "advancement_line_ids.payment_id",
        "advancement_line_ids.order_id",
        "advancement_line_ids.amount_imputed",
    )
    def _compute_amount_residual(self):
        for order in self:
            amount_imputed = 0.0
            amount_residual = order.amount_total
            for line in order.advancement_line_ids:
                if line.state in ("imputed", "draft"):
                    amount_imputed += line.amount_imputed
            amount_residual = amount_residual - amount_imputed
            order.update(
                {
                    "calcule_amount_residual": amount_residual,
                    "calcule_amount_imputed": amount_imputed,
                }
            )
    
    @api.multi
    def action_cancel(self):
        for lines in self.advancement_line_ids:
            lines.cancel()
            lines.unlink()
        return super(SaleOrder, self).action_cancel()