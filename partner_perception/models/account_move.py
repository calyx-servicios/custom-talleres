# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    def partner_perceptions(self):
        aml_obj = self.env["account.move.line"]
        for rec in self:
            if rec.invoice_date:
                date_alic_partner = rec.partner_id.arba_alicuot_ids.filtered(lambda v: v.from_date < rec.invoice_date < v.to_date)
                if date_alic_partner:
                    for line in rec.invoice_line_ids:
                        for tax in date_alic_partner.tag_id.tax_ids:
                            line.tax_ids = [(4, tax.id)]
                            amount = line.price_subtotal * date_alic_partner.alicuota_percepcion / 100
                            line_tax = tax.invoice_repartition_line_ids.filtered(lambda v: v.repartition_type == "tax")
                            line_id_tax = aml_obj.search([("tax_line_id","=",tax.id),("move_id","=",rec.id)])
                            if line_id_tax:
                                new_amount = line_id_tax.credit + amount
                                aml_obj.browse(line_id_tax.id).with_context(check_move_validity=False).write({"credit":new_amount})
                            else:
                                vals = {
                                    "account_id": line_tax.account_id.id,
                                    "name": tax.name,
                                    "tax_repartition_line_id": line_tax.id,
                                    "tax_line_id": tax.id,
                                    "tag_ids": line_tax.tag_ids.ids,
                                    "credit": amount,
                                    "exclude_from_invoice_tab": True,
                                    "move_id": rec.id
                                }
                                aml_obj.with_context(check_move_validity=False).create(vals)
                        debit_line = rec.line_ids.filtered(lambda v: v.credit == 0)
                        debit_line.debit = sum(rec.line_ids.filtered(lambda l: l.credit != 0).mapped("credit"))
                else:
                    raise ValidationError(_('This partner has not Alícuotas PERC-RET or the dates do not match'))
            else:
                raise ValidationError(_('This invoice has not date. For use partner perception this need a date'))

