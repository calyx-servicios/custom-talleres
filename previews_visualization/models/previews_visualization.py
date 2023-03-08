from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    
    advance = fields.Monetary(
        string="Advance",
        readonly=True,
        compute="_compute_advance",
    )

    @api.depends("advance")
    def _compute_advance(self):
        for rec in self:
            rec.advance = rec.amount_total-rec.calcule_amount_residual