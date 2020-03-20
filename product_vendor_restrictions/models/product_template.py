from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    purchase_ok = fields.Boolean('Can be Purchased', default=False)
