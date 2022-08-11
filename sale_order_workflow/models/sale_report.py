from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    sale_order_zone_ids = fields.Many2one("sale.order.zone", string="Zone")


    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.zone_ids as sale_order_zone_ids
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.zone_ids"
        return group_by_str
