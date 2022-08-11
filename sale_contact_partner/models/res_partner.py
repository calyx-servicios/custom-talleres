from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "res.partner"

    sale_zone_ids = fields.Many2one(comodel_name="sale.order.zone")


    @api.constrains("email")
    def _check_valid_email(self):
        for record in self:
            if " " in record.email:
                raise UserError(_("Email cannot have spaces ' '"))
            if "@" not in record.email or ".com" not in record.email:
                raise UserError(_("Please introduce a valid email"))
