from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_line_ids = fields.Many2one(comodel_name="sale.order.line")
    design = fields.Boolean(related="sale_order_line_ids.to_design", store=True)
