from odoo import models, fields


class SearchAssistant(models.TransientModel):
    _inherit = "search.assistant.line"


    to_quote = fields.Boolean()
    to_design = fields.Boolean()
    