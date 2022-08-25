from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re


EMAIL_CHECKUP = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_zone_id = fields.Many2one(comodel_name="partner.zone")


    def validity_email(self, email):
        if email:
            if not 5 < len(email) < 121 or not re.fullmatch(EMAIL_CHECKUP, email):
                return True
            else:
                return False


    @api.onchange("email")
    def _onchange_valid_email(self):
        if self.email and self.validity_email(self.email):
            raise UserError(_("Invalid Email"))

