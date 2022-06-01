from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    pickup_store = fields.Many2one('sale.store', string='Pick Up by Store')


    