from odoo import models, fields, api
from datetime import timedelta
import dateutil.parser


class SaleOrder(models.Model):
    _inherit = "sale.order"


    confirmation_date_no_time = fields.Date()
    date_order_date = fields.Date()
    sale_order_date = fields.Date(related="date_order_date", string="Request Date", store=True)


    @api.model
    def fields_get(self, fields=None, attributes=None):
        hide = ['confirmation_date',"date_order"]
        res = super(SaleOrder, self).fields_get()
        for field in hide:
            res[field]['selectable'] = False
        return res


    @api.model
    def create(self, vals):
        if vals.get("date_order",False):
            vals["date_order_date"] = dateutil.parser.parse(vals.get("date_order", False)).date()
            vals["sale_order_date"] = dateutil.parser.parse(vals.get("date_order", False)).date()
        if vals.get("confirmation_date",False):
            vals["confirmation_date_no_time"] = dateutil.parser.parse(vals.get("confirmation_date", False)).date()
        return super(SaleOrder, self).create(vals)

    @api.model
    def write(self, vals):
        if vals.get("date_order",False):
            vals["date_order_date"] = dateutil.parser.parse(vals.get("date_order", False)).date()
            vals["sale_order_date"] = dateutil.parser.parse(vals.get("date_order", False)).date()
        if vals.get("confirmation_date",False):
            vals["confirmation_date_no_time"] = dateutil.parser.parse(vals.get("confirmation_date", False)).date()
        return super(SaleOrder, self).write(vals)
