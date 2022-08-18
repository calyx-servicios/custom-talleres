from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_zone_ids = fields.Many2one("res.partner.partner_zone_ids", string="Zone")


    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , s.partner_zone_ids as partner_zone_ids
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", s.partner_zone_ids"
        return group_by_str
