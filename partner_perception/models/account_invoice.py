# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, _
from odoo.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def partner_perceptions(self):
        aml_obj = self.env["account.invoice.line"]
        for rec in self:
            if rec.date_invoice:
                date_alic_partner = rec.partner_id.arba_alicuot_ids.filtered(lambda v: v.from_date < rec.date_invoice < v.to_date)
                if date_alic_partner:
                    for line in rec.invoice_line_ids:
                        for tax in date_alic_partner.tag_id.tax_ids:
                            line.tax_ids = [(4, tax.id)]
                            amount = line.price_subtotal * date_alic_partner.alicuota_percepcion / 100
                            #Migra 13 - 11 es necesario crear un selection para filtrar que tipo de repartition es un impuesto
                            #line_tax = tax.invoice_repartition_line_ids.filtered(lambda v: v.repartition_type == "tax") 
                            line_id_tax = self.env['account.invoice.tax'].search([("tax_id","=",tax.id),("invoice_id","=",rec.id)])
                            if line_id_tax:
                                new_amount = line_id_tax.amount_total + amount
                                aml_obj.browse(line_id_tax.id).write({"amount_total":new_amount})
                            else:
                                vals = {
                                    "account_id": line_id_tax.account_id.id,
                                    "name": tax.name,
                                    #"tax_repartition_line_id": line_id_tax.id,  Migra 13 - 11
                                    #"tax_line_id": tax.id,                   Migra 13 - 11
                                    "tax_id": line_id_tax.tax_id.id,
                                    "amount_total": amount,
                                    #"exclude_from_invoice_tab": True,        Migra 13 - 11
                                    "invoice_id": rec.id
                                }
                                self.env['account.invoice.tax'].create(vals)
                        #debit_line = rec.line_ids.filtered(lambda v: v.credit == 0)                                    Migra 13 - 11
                        #debit_line.debit = sum(rec.line_ids.filtered(lambda l: l.credit != 0).mapped("credit"))        Migra 13 - 11
                else:
                    raise ValidationError(_('This partner has not Alícuotas PERC-RET or the dates do not match'))
            else:
                raise ValidationError(_('This invoice has not date. For use partner perception this need a date'))

