from odoo import models, fields, api

class MRPProduction(models.Model):
    _inherit = "mrp.production"

    def mass_cancel(self,records):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.mrp.mass.cancel',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': {'default_sale_order_ids':[(6, 0, records.ids)],},
        }
        