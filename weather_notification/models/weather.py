# -*- coding: utf-8 -*-

from odoo import models,api, fields


class Confsetting(models.TransientModel):
    """Give new fields related to weather details"""
    _inherit = "res.config.settings"

    weather = fields.Boolean(config_parameter='weather_notification.weather', string="Weather")
    api_key = fields.Char(config_parameter='weather_notification.api_key', string="API Key")
    city = fields.Char(config_parameter='weather_notification.city', string="City")

    @api.model
    def conf_details(self):
        """to give values to js"""
        get_param = self.env['ir.config_parameter'].sudo().get_param
        api_keys = get_param('weather_notification.api_key')
        weather = get_param('weather_notification.weather')
        city = get_param('weather_notification.city')
        data = {
            'api_keys': api_keys,
            'weather': weather,
            'city': city
        }
        return data
