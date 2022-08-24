from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    email_partner = fields.Char(related="partner_id.email")
    partner_zone = fields.Char(related="partner_id.partner_zone_id.name", store=True)
