from odoo import fields, models


class WarrantyInvoice(models.Model):
    _inherit = 'stock.picking'

    name = fields.Char()
    track_ids = fields.One2many('order.tracking', 'track_id')


class TrackOrders(models.Model):
    _name = "order.tracking"

    location_id = fields.Many2one('stock.location', string="Source Location")
    destination_id = fields.Many2one('stock.location', string="Destination Location")
    track_id = fields.Many2one('stock.picking')
