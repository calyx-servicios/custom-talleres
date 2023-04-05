from odoo import models, _
from odoo.exceptions import ValidationError

class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.report_sale_personalized_xls_copy.sale_report_xml'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Report Sale Personalized')
        bold = workbook.add_format({'bold': True})
        n = 1
        sheet.merge_range('A1', _('DETAILS'), )
        sheet.set_column('B:B', 1)
        sheet.set_column('B:B', 50)
        sheet.set_column('C:C', 1)
        sheet.set_column('C:C', 18)
        sheet.set_column('D:D', 1)
        sheet.set_column('D:D', 18)
        sheet.set_column('E:E', 1)
        sheet.set_column('E:E', 18)
        sheet.set_column('F:F', 1)
        sheet.set_column('F:F', 18)
        sheet.set_column('G:G', 1)
        sheet.set_column('G:G', 18)
        sheet.set_column('H:H', 1)
        sheet.set_column('H:H', 18)
        sheet.set_column('I:I', 1)
        sheet.set_column('I:I', 18)
        sheet.set_column('J:J', 1)
        sheet.set_column('J:J', 18)
        sheet.set_column('K:K', 1)
        sheet.set_column('K:K', 18)
        sheet.write('A1', 'Date', bold)
        sheet.write('B1', 'Client', bold)
        sheet.write('C1', 'Zone', bold)
        sheet.write('D1', 'City', bold)
        sheet.write('E1', 'Product', bold)
        sheet.write('F1', 'Brand', bold)
        sheet.write('G1', 'Price Total', bold)
        sheet.write('H1', 'Quantity', bold)
        sheet.write('I1', 'Discount', bold)
        sheet.write('J1', 'Sales Channel', bold)
        sheet.write('K1', 'Payment Method', bold)
        for obj in partners:
            qty_product = sum(obj.order_line.mapped("product_uom_qty"))
            disc = sum(obj.order_line.mapped("discount"))
            product_name = ''
            brand_name = ''
            payment = ''
            for line in obj.order_line:
                product_name += line.template_id.name + ' '
            for brand in obj.brand_ids:
                brand_name += brand.name
            for advan in obj.advancement_line_ids:
                p = advan.payment_id.payment_ids.mapped("payment_method_id")
                payment += p.name + ' '

            sheet.write(n, 0, obj.confirmation_date)
            sheet.write(n, 1, obj.partner_id.name)
            sheet.write(n, 2, obj.partner_id.partner_zone_id.name)
            sheet.write(n, 3, obj.partner_id.city)
            sheet.write(n, 4, product_name)
            sheet.write(n, 5, brand_name)
            sheet.write(n, 6, obj.amount_total)
            sheet.write(n, 7, qty_product)
            sheet.write(n, 8, disc)
            sheet.write(n, 9, obj.team_id.name)
            sheet.write(n, 10, payment)
            n+=1

       