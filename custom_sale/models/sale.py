# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging
_logger = logging.getLogger(__name__)

class saleOrder(models.Model):
    _inherit = 'sale.order'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, \
        readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, \
        help="Pricelist for current sales order.", default= lambda s: s.env['product.pricelist'].search([], limit=1))
    