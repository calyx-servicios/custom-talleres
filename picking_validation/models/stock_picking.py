from odoo import models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    
    @api.multi
    def button_validate(self):
        res  = super(StockPicking, self).button_validate()
        self.do_print_picking()
        return res