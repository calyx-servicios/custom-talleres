from odoo import models, fields, _

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    type_attribute = fields.Selection([
        ("color",_("Color")),
        ("size",_("Size")),
        ("material",_("Material")),
        ("other",_("Other")),
    ], default="other", string="Type Attribute")

