import binascii
import xlrd
from odoo import fields, models
from odoo.exceptions import UserError


class LotSerial(models.TransientModel):
    """to create a wizard in inventory module"""
    _name = "lot.serial"

    lot_serial = fields.Binary()
    file_name = fields.Char()

    def import_lot_serial(self):
        """ to import excel file """
        try:
            data = binascii.a2b_base64(self.lot_serial)
            book = xlrd.open_workbook(file_contents=data)
            # sheet = book.sheet_by_index(0)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        for sheet in book.sheets():
            try:
                if sheet.name == "Sheet1":
                    for row in range(sheet.nrows):
                        if row >= 1:
                            row_values = sheet.row_values(row)
                            vals = self._create_lot_serial(row_values)
                            if not vals:
                                continue
                            else:
                                self.env['stock.lot'].create(vals)
                    return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': 'lot and serial number imported'

                        }
                    }

            except IndexError:
                pass

    def _create_lot_serial(self, record):
        """create lot and serial number in stock.lot when imported"""
        product_id = self.env['product.template'].search([('name', '=', record[2])])
        lot = self.env['stock.lot'].search([('name', '=', record[0])])
        if lot or record[0] == "" or record[2] == "":
            return False
        if not product_id:
            product_id = self.env['product.product'].create({
                'name': record[2]
            })
        line_ids = {
            'name': record[0],
            'product_id': product_id.product_variant_id.id,
            'ref': record[1],
        }
        return line_ids
