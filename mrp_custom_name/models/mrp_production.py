from odoo import models,fields,api, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    _sql_constraints = [
        (
            "otis_number",
            "unique(otis_number)",
            _("OTIS Number must be unique!"),
        )
    ]
    otis_number = fields.Integer()

    @api.model
    def create(self, vals):
        if not vals.get("origin"):
                prefix = "OTIS/"
                name = prefix + str(vals["otis_number"])
        vals["name"] = name
        res = super(MrpProduction, self).create(vals)
        return res