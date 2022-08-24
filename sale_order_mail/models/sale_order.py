# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    email_partner = fields.Char(string="Email")

    def action_custom_email_send(self):
        self.ensure_one()

        body = (
            "<p>Estimado <strong>"
            + str(self.email_partner)
            + "</strong></p> \n <p>Le enviamos el presupuesto "
        )
        body += "<strong>" + str(self.name) + "</strong> de importe <strong>"
        body += (
            str(self.amount_total)
            + "</strong> desde "
            + str(self.company_id.name)
            + ".</p><br/>"
        )
        body += (
            "<center><span style='color:#888888'>(Vea el PDF adjunto)"
            "</span></center>"
        )
        body += "<br/><p>Para cualquier duda puede responder a este email.</p>"
        body += "<p>Muchas gracias,</p>"

        subject = str(self.company_id.name)
        if self.state in ("draft", "sent"):
            subject += " Presupuesto"
        else:
            subject += " Orden"
        subject += " Ref " + str(self.name)

        x = ""

        if self.user_id and self.user_id.signature:
            x = self.user_id.signature
        body += "<p style='color:#eeeeee;'>" + str(x) + "</p>"

        ctx = {
            "sale_id": self.ids[0],
            "default_body_email": body,
            "default_email_to": self.email_partner,
            "default_subject": subject,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "sale.order.mail.wizard",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
