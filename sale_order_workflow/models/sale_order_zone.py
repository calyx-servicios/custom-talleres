from odoo import models, fields, api


class SaleZone(models.Model):
    _name="sale.order.zone"

    name= fields.Char()
    description = fields.Char()
    