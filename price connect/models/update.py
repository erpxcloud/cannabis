# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
import xmlrpc.client
import json


class SaleOrderInherit(models.Model):
    _inherit = 'product.pricelist.item'

    remote_id = fields.Char(string='Remote ID', required=True,  track_visibility="always")


class UpdatePrices(models.Model):
    _name = 'update.prices'
    _description = 'Update Prices'

    def set_last_update(self):
        matches = self.env['ir.cron'].sudo().search_read([('model_id', '=', "Update Prices")], ['nextcall'])
        self.last_update = matches[0]['nextcall']

    url_db = fields.Char(string='URL', required=True,  track_visibility="always")
    db = fields.Char(string='Database', required=True,  track_visibility="always")
    username = fields.Char(string='Username', required=True,  track_visibility="always")
    password = fields.Char(string='Password', required=True,  track_visibility="always")
    update_date = fields.Datetime(string='Update Date')
    last_update = fields.Date(string='Last Update', readonly=True, compute=set_last_update)
    remote_id = fields.Char(string='Remote ID', required=True,  track_visibility="always")

    def action_button_test(self):
        f = open('/home/hadi/Documents/70.32.30.112.json', )
        data = json.load(f)
    #    print(data[0]['Date'])
        for i in data:
            matches = self.env['product.pricelist.item'].sudo().search_read([('remote_id', '=', i['Barcode'])], )
            match = matches[0]
            self.env['product.pricelist.item'].sudo().browse(match.write({'fixed_price': i['Retail Price']}))
