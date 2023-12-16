from odoo import fields, models


class ToleranceWizard(models.TransientModel):
    _name = "tolerance.wizard"

    stock_id = fields.Many2one('stock.picking')

    def accept_tolerance(self):
        self.stock_id.accept_check = True
        self.stock_id.button_validate()


