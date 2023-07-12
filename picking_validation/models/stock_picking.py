from odoo import models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    
    @api.multi
    def button_validate(self):
        res  = super().button_validate()
        self.do_print_picking()
        return res
    
    @api.multi
    def do_print_picking(self):
        self.write({"printed": True})
        return self.env.ref("stock.action_report_delivery").report_action(self)
    