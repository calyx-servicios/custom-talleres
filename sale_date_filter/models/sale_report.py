from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"


    confirmation_date_no_time = fields.Date()

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.confirmation_date_no_time as confirmation_date_no_time
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.confirmation_date_no_time"
        return group_by_str
   
    @api.model
    def fields_get(self, fields=None):
        hide = ['confirmation_date']
        res = super(SaleReport, self).fields_get()
        for field in hide:
            res[field]['selectable'] = False
        return res
