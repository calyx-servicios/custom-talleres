from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning



class SaleOrderAdvancement(models.Model):
    _name = "sale.order.advancement"
    _description = "Sale Order Advancement"
  

### Fields
    name = fields.Char(string='Description')
    payment_id = fields.Many2one('account.payment.group', required=True, string='Payment',ondelete='cascade' )
    order_id = fields.Many2one('sale.order', required=True, string='Sale Order',ondelete='cascade' )
    amount_imputed = fields.Float(string='Amount Imputed', required=True)
    state = fields.Selection([('imputed','Imputed'),
                              ('cancel','Cancel'),
                             ], string='State',default='imputed')
### ends Field

    @api.multi
    def cancel(self):
        for self_obj in self: 
            #self_obj.state = 'cancel'
            self_obj.payment_id.boolean_total_imputed = False
            self_obj.unlink()
            