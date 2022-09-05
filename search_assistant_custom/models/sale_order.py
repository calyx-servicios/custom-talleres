from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order_date = fields.Date(string="Fecha Presupuesto")

    # @api.multi
    # def _compute_date_order_date(self):
    #     for order in self:
    #         order.date_order_date = order.date_order


    # @api.depends("date_order")
    # def _compute_date_order_date(self):
    #     for order in self:
    #         order.update({"date_order_date": order.date_order})