from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_zone_ids = fields.Many2one(comodel_name="res.partner")
    partner_zone_ids_name =fields.Char(related="partner_zone_ids.name")

    email_partner = fields.Char(related="partner_id.email")
    partner_zone = fields.Char(related="partner_id.partner_zone_ids.name", store=True)
