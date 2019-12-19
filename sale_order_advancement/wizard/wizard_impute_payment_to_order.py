from odoo import models, api, fields, _
from ast import literal_eval
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class ImputePaymentToOrder(models.TransientModel):

    _name = 'impute.payment.to.order'
    _description = 'Impute Payment To Order'


    @api.onchange('payment_id')
    def _onchange_payment_id(self):
        amount=0.0
        for line in self:
            line.amount_payment = line.payment_id.amount_to_impute 
            
### Fields
    name = fields.Char(string='Description')
    payment_id = fields.Many2one('account.payment.group', string='Payment',)
    amount = fields.Float(string='Amount', )
    amount_payment = fields.Float(string='Amount Payment', ) 
    partner_id = fields.Many2one('res.partner', string='Partner',)
### ends Field  < >


    @api.multi
    def impute_payment(self):
        for self_obj in self: 
            if (self_obj.payment_id.amount_to_impute) < self_obj.amount:
                raise ValidationError(_('You cant not Impute more of Payment has for impute.'))
            vals = {
                'name' : self_obj.name,
                'payment_id' : self_obj.payment_id.id,
                'amount_imputed' : self_obj.amount,
                'order_id': self._context['active_id'],    
            }
            advancement_obj = self.env['sale.order.advancement'].create(vals) 
