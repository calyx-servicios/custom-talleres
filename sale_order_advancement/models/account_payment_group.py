# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _

class AccountpPaymentGroup(models.Model):

    _inherit = "account.payment.group"

### Fields
    advancement_line_ids = fields.One2many('sale.order.advancement', 'payment_id', string='Advancement Lines',)
    amount_to_impute = fields.Monetary(string='Total', readonly=True, compute='_compute_amount_to_impute'  ) #
    boolean_total_imputed = fields.Boolean(string='Total Imputed',) #
### ends Field  < >



    @api.multi
    @api.depends('advancement_line_ids.payment_id', 'advancement_line_ids.order_id', 'advancement_line_ids.amount_imputed')
    def _compute_amount_to_impute(self):
        amount_to_impute = self.payments_amount
        for group_obj in self:
            for line in group_obj.advancement_line_ids:
                if line.state == 'imputed':
                    amount_to_impute -= line.amount_imputed
            group_obj.amount_to_impute = amount_to_impute
            print(' a ver que apsa aca')
            print(' a ver que apsa aca')
            print(amount_to_impute)
            print(' a ver que apsa aca')
            if amount_to_impute > 0.001:
                print('    entro al false')
                print('    entro al false')
                group_obj.write({'boolean_total_imputed':False}) 
            else:
                print('    entro al True')
                print('    entro al true')
                group_obj.write({'boolean_total_imputed':True})  
            print(' a ver que apsa aca')
            print(' a ver que apsa aca')
        