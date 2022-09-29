from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"


    design = fields.Boolean()


    @api.model
    def create(self, vals):
        res = super(MrpProduction, self).create(vals)
        if len(res.sale_id.production_ids)>1:
            line = res.sale_id.order_line[len(res.sale_id.production_ids)-1]
            res.design = line.to_design
        return res
        