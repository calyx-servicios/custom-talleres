# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
import psycopg2

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attachment_ids = fields.Many2many(
        'ir.attachment', 'product_ir_attachments_rel','template_id', 'attachment_id', 'Attachments')
