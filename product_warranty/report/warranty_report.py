from odoo import models, api
from odoo.exceptions import ValidationError


class WarrantyReport(models.AbstractModel):
    _name = 'report.product_warranty.report_warranty'

    @api.model
    def _get_report_values(self, docids, data=None):
        customer_id = data['form_data']['customer_id']
        product_ids = data['form_data']['product_ids']
        products_name = data['products']
        start_date = data['form_data']['start_date']
        end_date = data['form_data']['end_date']

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
            'customer_id': customer_id,
            'product_ids': product_ids,
            'products_name': products_name,
            'start_date': start_date,
            'end_date': end_date,
            'report': report
        }
        print(data)

        return {
            'doc_ids': docids,
            'doc_model': 'product.warranty',
            'data': data,
        }
