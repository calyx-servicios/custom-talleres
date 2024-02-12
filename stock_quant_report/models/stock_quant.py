from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    real_stock = fields.Float(string='Real Stock',compute='_compute_stock')

    @api.depends('quantity', 'reserved_quantity')
    def _compute_stock(self):
        for stock in self:
            stock.real_stock = stock.quantity * stock.reserved_quantity

    
