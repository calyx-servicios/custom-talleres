# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"
  

    advancement_line_ids = fields.One2many('sale.order.advancement', 'order_id', string='Advancement Lines',)
    calcule_amount_imputed = fields.Monetary(string='Total', readonly=True,compute='_compute_amount_imputed' ) #
    
    @api.multi
    @api.depends('advancement_line_ids.payment_id', 'advancement_line_ids.order_id', 'advancement_line_ids.amount_imputed')
    def _compute_amount_imputed(self):
        amount_imputed = 0.0
        for order_obj in self:
            for line in order_obj.advancement_line_ids:
                amount_imputed += line.amount_imputed
            order_obj.calcule_amount_imputed = amount_imputed

