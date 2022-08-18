from odoo import models, fields, api


class PartnerZone(models.Model):
    _name = "partner.zone"


    name = fields.Char(required=True)
    description = fields.Char
    