from odoo import api, fields, models


class SaleOrderAdvancement(models.Model):
    _name = "sale.order.advancement"
    _description = "Sale Order Advancement"

    # ## Fields
    name = fields.Char(string="Description")
    payment_id = fields.Many2one(
        "account.payment.group",
        required=True,
        string="Payment",
        ondelete="cascade",
    )
    order_id = fields.Many2one(
        "sale.order", required=True, string="Sale Order", ondelete="cascade"
    )
    amount_imputed = fields.Float(string="Amount Imputed", required=True)
    state = fields.Selection(
        [("imputed", "Imputed"), ("cancel", "Cancel"), ("draft", "Draft")],
        string="State",
        compute="_calculate_state",
    )
    # ## ends Field

    @api.multi
    def cancel(self):
        for self_obj in self:
            # self_obj.state = 'cancel'
            self_obj.payment_id.boolean_total_imputed = False
            self_obj.unlink()

    @api.depends("order_id.state")
    def _calculate_state(self):
        for record in self:
            if record.order_id:
                if record.order_id.state == "draft":
                    record.update({"state": "draft"})
                else:
                    record.update({"state": "imputed"})
