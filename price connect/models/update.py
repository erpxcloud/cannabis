# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
import xmlrpc.client


class SaleOrderInherit(models.Model):
    _inherit = 'product.pricelist'

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
    update_date = fields.Date(string='Update Date')
    last_update = fields.Date(string='Last Update', readonly=True, compute=set_last_update)
    remote_id = fields.Char(string='Remote ID', required=True,  track_visibility="always")

    def action_button_test(self):
        url_db = self.url_db
        db = self.db
        username = self.username
        password = self.password
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db))
        models2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db))

        uid_db = common.authenticate(db, username, password, {})

        products = models2.execute_kw(db, uid_db, password, 'product.template', 'search_read',
                                        [[['write_date', '>', self.update_date]]],
                                         {'fields': ['list_price']})
        initial_number = len(products)
        print(initial_number)
        print("products", products)
        for product in products:
            matches = self.env['product.template'].sudo().search_read([('remote_id', '=', product['id'])], ['id'])
            match = matches[0]
            self.env['product.template'].sudo().browse(match['id']).write({'list_price': product['list_price']})
