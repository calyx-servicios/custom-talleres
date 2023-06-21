from odoo import models, fields


class WizardMRPMassCancel(models.TransientModel):
    _name = 'wizard.mrp.mass.cancel'
    _description = 'Mass Cancel'
    
    mrp_production_ids = fields.Many2many('mrp.production')

    def confirm(self):
        for line in self.mrp_production_ids:
            line.action_cancel()