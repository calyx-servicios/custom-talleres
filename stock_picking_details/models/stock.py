# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    elevator = fields.Boolean(string="Elevator", required=True, default=False)
    staircase = fields.Boolean(
        string="Staircase", required=True, default=False
    )
    exterior_access = fields.Boolean(
        string="Exterior Access", required=True, default=False
    )
    req_authorization = fields.Boolean(
        string="Req Authorization", required=True, default=False
    )    
    calcule_amount_residual = fields.Float(
        string="Amount Residual",
        compute="_compute_amount_residual"
    )
          
    @api.model
    def _compute_amount_residual(self):
        for rec in self:
            i = 0
            total_amount_residual = 0.00
            double_orders = []
            if rec.origin:
                origin = rec.origin.split()
                simple_orders = rec.origin.split()
                for order in origin:
                    if order == "-":
                        double_orders += [origin[i-1] + " " + order + " " + origin[i+1]]
                        if origin[i-1]:
                            simple_orders.remove(origin[i-1])
                        simple_orders.remove(order)
                        simple_orders.remove(origin[i+1])
                    i += 1
                
                simple_orders.extend(double_orders)
                for order in simple_orders:
                    record = self.env['sale.order'].search([('name', '=', order)], limit=1)
                    if record and record.calcule_amount_residual:
                        total_amount_residual += record.calcule_amount_residual
    
            rec.calcule_amount_residual = total_amount_residual

    def button_validate(self):
        if not self.pickup_store:
            if self.calcule_amount_residual > 0:
                raise UserError(_('You still have balance to pay on this order!'))

        return super().button_validate()

