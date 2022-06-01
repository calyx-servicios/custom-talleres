from odoo import models, fields

class SaleStore(models.Model):
    _name = 'sale.store'
    _description = 'Stores for pick up'
    
    name = fields.Char('Name store')
    active = fields.Boolean('Active', default=True)

