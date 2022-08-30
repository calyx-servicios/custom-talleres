from odoo import models, fields, api
from datetime import timedelta
import dateutil.parser


class SaleOrder(models.Model):
    _inherit = "sale.order"


    confirmation_date_no_time = fields.Date(compute="_get_confirmation_date", store=True)
    date_order_date = fields.Date()


    @api.multi
    def _get_confirmation_date(self):
        for record in self:
            if record.confirmation_date:
                date = dateutil.parser.parse(record.confirmation_date).date()
                record.update({"confirmation_date_no_time": date})


    @api.model
    def fields_get(self, fields=None):
        hide = ['confirmation_date']
        res = super(SaleOrder, self).fields_get()
        for field in hide:
            res[field]['selectable'] = False
        return res