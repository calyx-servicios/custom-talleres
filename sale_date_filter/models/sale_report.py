from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"


    confirmation_date_no_time = fields.Date()
    date_order_date = fields.Date(string="FECHA DE PEDIDO")
    sale_order_date  = fields.Date(string="Request Date")

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """

            , s.confirmation_date_no_time as confirmation_date_no_time,
              s.date_order_date as date_order_date,
              s.sale_order_date as sale_order_date
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.confirmation_date_no_time, s.date_order_date, s.sale_order_date"
        return group_by_str
   
    @api.model
    def fields_get(self, fields=None, attributes=None):
        hide = ['confirmation_date','date']
        res = super(SaleReport, self).fields_get()
        for field in hide:
            res[field]['selectable'] = False
            res[field]['store'] = False
        return res
