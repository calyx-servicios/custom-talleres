# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "product_ir_attachments_rel",
        "template_id",
        "attachment_id",
        "Attachments",
    )

