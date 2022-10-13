from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    from_design = fields.Selection(
        [
            ("mrp_without_design", "Without design"),
            ("mrp_from_design", "From design"),
        ],
        string="From design", default="mrp_without_design")
        