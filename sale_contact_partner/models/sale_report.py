from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_zone = fields.Char(string="Zone")


    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.partner_zone as partner_zone
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.partner_zone"
        return group_by_str
