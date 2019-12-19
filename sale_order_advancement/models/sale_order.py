# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError



# variable de nuevas lineas en sale order.. con sale.order a account.invoice  y un MONTO UTILIZADO y al revez..

# campo caculado en invoice con el monto que le resta "usar" de la factura (calculado con el one2many de arriba)
# campo caculado en order con el monto que le resta "pagar" de la factura (calculado con el one2many de arriba)

# WIZARD QUE solicita facturas y ordenes de pagos.. hace una matris para ingresar montos.. CREA LAS LINEAS 
# CORRESPONDIENTES (controlando que no se sobre pague la orden y que no utilice mas monto que el permitido en la factura...)


class SaleOrder(models.Model):
    _inherit = "sale.order"


    #
        

    advancement_line_ids = fields.One2many('sale.order.advancement', 'order_id', string='Advancement Lines',)
    calcule_amount_imputed = fields.Monetary(string='Total', readonly=True,compute='_compute_amount_imputed' ) #
    
    @api.multi
    @api.depends('advancement_line_ids.payment_id', 'advancement_line_ids.order_id', 'advancement_line_ids.amount_imputed')
    def _compute_amount_imputed(self):
        amount_imputed = 0.0
        for line in self.advancement_line_ids:
            amount_imputed += line.amount_imputed
        self.calcule_amount_imputed = amount_imputed