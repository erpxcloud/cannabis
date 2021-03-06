# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
import xmlrpc.client
import json
import requests
import logging
from datetime import datetime


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

    def action_button_test(self):
        #with urllib.request.urlopen("http://70.32.30.112:8035/") as url:
        #data = json.loads(url.read().decode())
        
        values = {}
        data = json.loads(requests.get("http://70.32.30.112:8035/").text)
    #    print(data[0]['Date'])
        for i in data:
            iupdate_date = datetime.strptime(data[0]['Date'], '%Y-%m-%d %H:%M:%S')
            if self.update_date < iupdate_date :
                matches = self.env['product.pricelist.item'].sudo().search_read([('remote_id', '=', i['Barcode'])], )
                for match in matches:
                     qty = match['min_quantity']
                     if qty== 0:
                        qty =1
                     pricelist = self.env['product.pricelist.item'].browse(match['id']).sudo()
                     values['fixed_price'] = i['Retail Price']/qty
                     pricelist.write(values)
                     #pricelist = self.env['product.pricelist.item'].sudo().browse(match.id)  
                     #print(pricelist.remote_id)
                     #print(pricelist.id)
                     #pricelist.sudo().write({'fixed_price': i['Retail Price']})
