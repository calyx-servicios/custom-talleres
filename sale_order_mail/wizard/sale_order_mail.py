from odoo import models, api, fields
import base64

import logging

_logger = logging.getLogger(__name__)


class SaleOrderMailWizard(models.TransientModel):
    _name = "sale.order.mail.wizard"
    _inherit = ["mail.thread"]
    _description = "Sale Order Wizard Email"

    @api.model
    def _default_sale_id(self):
        if self._context.get("sale_id"):
            sale_id = self._context.get("sale_id")
            return sale_id

    sale_id = fields.Many2one(
        "sale.order", string="Sale Order", default=_default_sale_id
    )
    email_to = fields.Char(string="Email to")
    body_email = fields.Html(string="Body")
    subject = fields.Char(string="Subject")

    mail_server_id = fields.Many2one(
        'ir.mail_server',
        string = 'Mail Server'
    )

    def _action_generate_email_attachment(self):
        if self._context.get("sale_id"):
            sale_id = self._context.get("sale_id")
        else:
            return {}

        attachment_model = self.env["ir.attachment"]

        data = (
            self.env.ref("sale.action_report_saleorder")
            .sudo()
            .render_qweb_pdf([sale_id])[0]
        )
        pdf = base64.b64encode(data)

        name = self.env["sale.order"].browse(sale_id).name
        ATTACHMENT_NAME = str(name)
        vals = {
            "name": ATTACHMENT_NAME + ".pdf",
            "res_model": self._name,
            "res_id": self.id,
            "datas_fname": ATTACHMENT_NAME + ".pdf",
            "store_fname": ATTACHMENT_NAME,
            "datas": pdf,
            "mimetype": "application/pdf",
            "type": "binary",
        }
        attachments_record = attachment_model.sudo().create(vals)
        return attachments_record.ids

    attachment_ids = fields.Many2many(
        "ir.attachment", default=_action_generate_email_attachment
    )

    @api.multi
    def send_mail_action(self):
        # CREAR CORREO Y ENVIAR
        template = self.env.ref(
            "sale_order_mail.email_template_sale_custom_partner"
        )
        for attachment in self.attachment_ids:
            template.attachment_ids = [(4, attachment.id)]

        mail_id = (
            self.env["mail.template"].browse(template.id).send_mail(self.id)
        )
        mail = self.env["mail.mail"].sudo().browse(mail_id)
        mail.write({"body_html": self.body_email})
        mail.write({"mail_server_id": self.mail_server_id.id})
        mail.send()
        for attachment in self.attachment_ids:
            template.attachment_ids = [(3, attachment.id)]
