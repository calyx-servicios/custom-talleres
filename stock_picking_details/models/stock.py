# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging

_logger = logging.getLogger(__name__)


class stockPicking(models.Model):

    _inherit = "stock.picking"
    elevator = fields.Boolean(string="Elevator", required=True, default=False)
    staircase = fields.Boolean(
        string="Staircase", required=True, default=False
    )
    exterior_access = fields.Boolean(
        string="Exterior Access", required=True, default=False
    )
    req_authorization = fields.Boolean(
        string="Req Authorization", required=True, default=False
    )
