# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
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
        compute="_compute_amount_residual",
        store=True
    )
          
    @api.one
    def _compute_amount_residual(self):
        i = 0
        total_amount_residual = 0.00
        double_orders = []
        if self.origin:
            origin = self.origin.split()
            simple_orders = self.origin.split()
            for order in origin:
                if order == "-":
                    double_orders += [origin[i-1] + " " + order + " " + origin[i+1]]
                    simple_orders.remove(origin[i-1])
                    simple_orders.remove(order)
                    simple_orders.remove(origin[i+1])
                i += 1
            
            simple_orders.extend(double_orders)
            for order in simple_orders:
                record = self.env['sale.order'].search([('name', '=', order)])
                if record.calcule_amount_residual:
                    total_amount_residual += record.calcule_amount_residual

        self.calcule_amount_residual = total_amount_residual