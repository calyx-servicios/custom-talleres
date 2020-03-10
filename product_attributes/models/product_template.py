# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attachment_ids = fields.Many2many(
        'ir.attachment', 'product_ir_attachments_rel', 'template_id', 'attachment_id', 'Attachments',
        help="Add one or several files related to the product")
