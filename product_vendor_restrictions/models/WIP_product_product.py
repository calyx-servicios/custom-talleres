from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.product"

    purchase_ok = fields.Boolean('Can be Purchased', default=False)
