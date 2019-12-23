# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"
  

    advancement_line_ids = fields.One2many('sale.order.advancement', 'order_id', string='Advancement Lines',)
    calcule_amount_residual = fields.Monetary(string='Amount Residual', readonly=True, compute='_compute_amount_residual' )
    
    @api.multi
    @api.depends('advancement_line_ids')
    def _compute_amount_residual(self):
        amount_imputed = 0.0
        for order_obj in self:
            for line in order_obj.advancement_line_ids:
                if line.state == 'imputed':
                    amount_imputed += line.amount_imputed
            order_obj.calcule_amount_residual = order_obj.amount_total - amount_imputed

