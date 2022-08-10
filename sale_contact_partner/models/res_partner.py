from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "res.partner"

    sale_zone_ids = fields.Many2one(comodel_name="sale.order.zone")
    