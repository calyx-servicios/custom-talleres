# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Production(models.Model):
    _inherit = 'mrp.production'
    attachment_ids = fields.Many2many(
        'ir.attachment', 'production_ir_attachments_rel','production_id', 'attachment_id', 'Attachments')

    
