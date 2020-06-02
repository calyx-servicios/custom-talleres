from odoo import models, api, fields


class ImputePaymentToOrder(models.TransientModel):

    _name = "impute.payment.to.order"
    _description = "Impute Payment To Order"

    # @api.onchange("payment_id")
    # def _onchange_payment_id(self):
    #     # amount = 0.0
    #     for line in self:
    #         line.amount_payment = line.payment_id.amount_to_impute

    # ## Fields
    name = fields.Char(string="Description")
    payment_id = fields.Many2one("account.payment.group", string="Payment",)
    amount = fields.Float(string="Amount",)
    amount_payment = fields.Float(string="Amount Payment",)
    partner_id = fields.Many2one("res.partner", string="Partner",)
    # ## ends Field  < >

    @api.multi
    def impute_payment(self):
        view = self.env.ref("sh_message.sh_message_wizard")
        context = dict(self._context or {})
        for self_obj in self:
            if (self_obj.payment_id.amount_to_impute) < self_obj.amount:
                title = "¡Advertencia!"
                context[
                    "message"
                ] = "No puede Imputar mas que lo que el Pago posee."
                return self.alert_message(title, view, context)
                # raise ValidationError(
                #     _("You cant not Impute more of Payment has for impute.")
                # )
            vals = {
                "name": self_obj.name,
                "payment_id": self_obj.payment_id.id,
                "amount_imputed": self_obj.amount,
                "order_id": self._context["active_id"],
            }
            self.env["sale.order.advancement"].create(vals)

            if self_obj.payment_id.amount_to_impute == self_obj.amount:
                self_obj.payment_id.boolean_total_imputed = True

    def alert_message(self, title, view, context):
        return {
            "name": title,
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sh.message.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": context,
        }
