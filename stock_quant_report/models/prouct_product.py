from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_values = fields.Monetary(string='Stock Value',compute='_compute_stock_value', currency_field='currency_id', store=True)

    @api.depends('qty_available', 'lst_price')
    def _compute_stock_value(self):
        for product in self:
            product.stock_values = product.qty_available * product.lst_price
