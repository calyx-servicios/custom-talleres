from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        invoice.account_id = invoice.partner_id.with_context(force_company=invoice.company_id.id).property_account_receivable_id.id
        return invoice
    
    @api.onchange('company_id')
    def _onchange_company(self):
        if self.journal_id:
            new_journal = ""
            if len(self.journal_id.name) > 20 and self.journal_id.name[:20] == "PROFORMA PRESUPUESTO":
                new_journal = self.env['account.journal'].search([('name', 'like' ,self.journal_id.name[:20]),('company_id', '=' ,self.company_id.id)])
            elif len(self.journal_id.name) > 12 and self.journal_id.name[:12] == "FACTURA AFIP":
                new_journal = self.env['account.journal'].search([('name', 'like' ,self.journal_id.name[:12]),('company_id', '=' ,self.company_id.id)])
            self.journal_id = new_journal    
        for line in self.invoice_line_ids:
            if line.product_id:
                line.account_id = line.product_id.with_context(force_company=line.company_id.id).categ_id.property_account_income_categ_id.id
            if len(line.invoice_line_tax_ids) != 0:
                tax_ids = []
                for tax in line.invoice_line_tax_ids:
                    new_tax = self.env['account.tax'].search([('name', '=' ,tax.name),('company_id', '=' ,line.company_id.id),('type_tax_use','=',tax.type_tax_use)])
                    tax_ids.append(new_tax.id)
                if len(tax_ids) != 0:
                    line.invoice_line_tax_ids = [(6,0,tax_ids)]