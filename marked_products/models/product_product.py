from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        if line.product_id.description_sale != False:
            line.name = line.product_id.name +" - "+ line.product_id.description_sale
        return line


