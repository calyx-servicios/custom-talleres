##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    brand_ids = fields.Many2many(
        'product.brand', 'users_brand_rel', 'user_id', 'brand_id', 'Brands')
