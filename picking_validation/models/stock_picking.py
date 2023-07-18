from odoo import models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    
    @api.multi
    def button_validate(self):
        res  = super(StockPicking, self).button_validate()
        return super(StockPicking, self).do_print_picking()