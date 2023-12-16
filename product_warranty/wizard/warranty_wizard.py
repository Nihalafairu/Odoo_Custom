import xlsxwriter
from odoo.exceptions import ValidationError
from odoo import fields, models
import json
from odoo.tools import date_utils
import io
from datetime import date


class ToleranceWizard(models.TransientModel):
    """this model is used for creating wizard"""
    _name = "warranty.wizard"

    product_ids = fields.Many2many('product.product', string="product", domain="[('has_warranty','=',True)]")
    customer_id = fields.Many2one('res.partner')
    start_date = fields.Date()
    end_date = fields.Date()

    def generate_pdf_report(self):
        """to generate pdf"""
        products = []
        for j in self.product_ids:
            products.append(j.name)
        data = {
            'form_data': self.read()[0],
            'products': products
        }
        return self.env.ref('product_warranty.action_report_product_warranty').report_action(None, data=data)

    def generate_xlsx_report(self):
        """to generate xlsx"""
        products = []
        for j in self.product_ids:
            products.append(j.name)
        data = {
            'form_data': self.read()[0],
            'products': products
        }
        customer_id = data['form_data']['customer_id']
        product_ids = data['form_data']['product_ids']
        start_date = data['form_data']['start_date']
        end_date = data['form_data']['end_date']
        product_name = data['products']
        query = """select account_move.name as invoice, res_partner.name as customer ,product_template.name 
                ::json->'en_US' as product, product_warranty.request_date,product_warranty.warranty_expire_date  
                from product_warranty 
                inner join
                account_move on account_move.id = product_warranty.invoice_id
                inner join 
                res_partner on res_partner.id = account_move.partner_id inner join product_product on product_product.id = 
                product_warranty.product_id
                inner join 
                product_template on product_template.id = product_product.product_tmpl_id"""

        query_connector = """ where """
        if customer_id:
            query += query_connector + """res_partner.id = '%s' """ % customer_id[0]
            query_connector = """ and """
        if product_ids:
            products = ', '.join(str(i) for i in product_ids)
            query += query_connector + """product_product.id in (%s) """ % products
            query_connector = """ and """
        if start_date:
            query += query_connector + """product_warranty.request_date >='%s' """ % start_date
            query_connector = """ and """
        if end_date:
            query += query_connector + """product_warranty.request_date <='%s' """ % end_date

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if not report:
            raise ValidationError('No Records to print')
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_ids': self.product_ids,
            'customer_id': self.customer_id.name,
            'product_name': product_name,
            'report': report,

        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'warranty.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """to get xlsx report"""
        from_date = data['start_date']
        to_date = data['end_date']
        report = data['report']
        customer_id = data['customer_id']
        product_name = data['product_name']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        status_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px'})

        sheet.merge_range('A1:C1', self.env.company.name, status_head)
        sheet.merge_range('A2:C2', self.env.company.city, status_head)
        sheet.merge_range('A3:C3', self.env.company.state_id.name, status_head)
        sheet.merge_range('A4:C4', self.env.company.country_id.name, status_head)
        sheet.merge_range('A6:C6', 'Created on:' + str(date.today()), status_head)

        sheet.merge_range('E8:J9', 'PRODUCT WARRANTY', head)
        if from_date:
            sheet.merge_range('B10:C10', 'From Date:', cell_format)
            sheet.merge_range('D10:E10', from_date, txt)
        if to_date:
            sheet.merge_range('B11:C11', 'To Date:', cell_format)
            sheet.merge_range('D11:E11', to_date, txt)

        if not customer_id and len(product_name) != 1:
            sheet.merge_range('A15:C15', 'Invoice', cell_format)
            sheet.merge_range('D15:E15', 'Customer', cell_format)
            sheet.merge_range('F15:H15', 'Product', cell_format)
            sheet.merge_range('I15:J15', 'Request Date', cell_format)
            sheet.merge_range('K15:M15', 'Expire Date', cell_format)
            row = 16
            for i in report:
                sheet.merge_range('A' + str(row) + ':C' + str(row), i['invoice'], txt)
                sheet.merge_range('D' + str(row) + ':E' + str(row), i['customer'], txt)
                sheet.merge_range('F' + str(row) + ':H' + str(row), i['product'], txt)
                sheet.merge_range('I' + str(row) + ':J' + str(row), i['request_date'], txt)
                sheet.merge_range('K' + str(row) + ':M' + str(row), i['warranty_expire_date'], txt)

                row += 1

        if customer_id and len(product_name) != 1:
            sheet.merge_range('B12:C12', 'Customer:', cell_format)
            sheet.merge_range('D12:E12', customer_id, txt)
            sheet.merge_range('A15:C15', 'Invoice', cell_format)
            sheet.merge_range('D15:E15', 'Product', cell_format)
            sheet.merge_range('F15:G15', 'Request', cell_format)
            sheet.merge_range('H15:J15', 'Expire Date', cell_format)
            row = 16
            for i in report:
                sheet.merge_range('A' + str(row) + ':C' + str(row), i['invoice'], txt)
                sheet.merge_range('D' + str(row) + ':E' + str(row), i['product'], txt)
                sheet.merge_range('F' + str(row) + ':G' + str(row), i['request_date'], txt)
                sheet.merge_range('H' + str(row) + ':J' + str(row), i['warranty_expire_date'], txt)

                row += 1

        if not customer_id and len(product_name) == 1:
            sheet.merge_range('B13:C13', 'Product:', cell_format)
            sheet.merge_range('D13:E13', product_name[0], txt)
            sheet.merge_range('A15:C15', 'Invoice', cell_format)
            sheet.merge_range('D15:E15', 'Customer', cell_format)
            sheet.merge_range('F15:H15', 'Request Date', cell_format)
            sheet.merge_range('I15:J15', 'Expire Date', cell_format)
            row = 16
            for i in report:
                sheet.merge_range('A' + str(row) + ':C' + str(row), i['invoice'], txt)
                sheet.merge_range('D' + str(row) + ':E' + str(row), i['customer'], txt)
                sheet.merge_range('F' + str(row) + ':H' + str(row), i['request_date'], txt)
                sheet.merge_range('I' + str(row) + ':J' + str(row), i['warranty_expire_date'], txt)

                row += 1

        if customer_id and len(product_name) == 1:
            sheet.merge_range('B12:C12', 'Customer:', cell_format)
            sheet.merge_range('D12:E12', customer_id, txt)
            sheet.merge_range('B13:C13', 'Product:', cell_format)
            sheet.merge_range('D13:E13', product_name[0], txt)
            sheet.merge_range('A15:C15', 'Invoice', cell_format)
            sheet.merge_range('D15:E15', 'Request Date', cell_format)
            sheet.merge_range('F15:H15', 'Expire Date', cell_format)
            row = 16
            for i in report:
                sheet.merge_range('A' + str(row) + ':C' + str(row), i['invoice'], txt)
                sheet.merge_range('D' + str(row) + ':E' + str(row), i['request_date'], txt)
                sheet.merge_range('F' + str(row) + ':H' + str(row), i['warranty_expire_date'], txt)

                row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

