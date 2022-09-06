from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order_date = fields.Date()
