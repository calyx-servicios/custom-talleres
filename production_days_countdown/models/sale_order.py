# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from datetime import datetime, date, timedelta
import dateutil.parser


class SaleOrder(models.Model):
    _inherit = "sale.order"


   
    @api.multi
    def production_days_count(self):
        
        for rec in self:
            actual_date = datetime.now()  
            actual_date = actual_date.date()  
            if rec.production_status == "to produce" or rec.production_status == "in produce":
                if rec.production_order:
                    if  rec.production_order.state != "cancel" and rec.production_order.state != "done":
                        start_date = datetime.strptime(rec.production_order.date_planned_start, "%Y-%m-%d %H:%M:%S")   
                        start_date = start_date.date() 
                        compromise_date = datetime.strptime(rec.production_order.compromise_date, "%Y-%m-%d")
                        compromise_date = compromise_date.date()
                        if start_date <= actual_date:
                            days =  actual_date - start_date
                            rec.update({"production_days": days})
                        elif actual_date > start_date and actual_date < compromise_date:
                            days =  actual_date - compromise_date 
                            rec.update({"production_days": days})
                        elif actual_date >= compromise_date:
                            days = compromise_date - actual_date
                            rec.update({"production_days": days})
            else:
                rec.update({"production_days": False})

    production_days = fields.Char(
        string="Production Countdown Days",
        compute="production_days_count",
    )
