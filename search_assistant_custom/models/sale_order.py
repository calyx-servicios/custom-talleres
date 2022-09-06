from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import dateutil.parser

class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order_date = fields.Date(string="Fecha Presupuesto")
