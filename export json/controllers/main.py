# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author:Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.addons.sale.controllers.onboarding import OnboardingController  # Import the class
from odoo.tools import html_escape
import io
from odoo import api, fields, models, _




class CustomOnboardingController(OnboardingController):  # Inherit in your custom class
    @http.route('/test', auth='user', type='http')
    def sale_quotation_onboarding(self):
        res = super(CustomOnboardingController, self).sale_quotation_onboarding()
        # Your code goes here
        return res


class MyController(http.Controller):
    @http.route('/some_url', auth='public')
    def handler(self):
        return {'attribute': 'test'}

class MyController(http.Controller):
    @http.route('/api/json_get_request', auth='public', type='http',  csrf=False)
    def printjson(self, **kw):
        data = {
        "params": {
            "name":"prakashsharma",
            "email":"prakashsharmacs24@gmail.com",
            "phone":"+917859884833"
                    }
                }
        print (data)
        print (json.dumps(data))
        return json.dumps(get_lines())
    
    
def get_lines():
        lines = []
        categ_products = request.env['product.product'].search([])
        for obj in categ_products:
            vals = {
                'sku': obj.default_code,
                'name': obj.name,
                'category': obj.categ_id.name,
                'cost_price': obj.standard_price,
                'quantity' : obj.qty_available,
                'barcode' : obj.barcode,
                'sale_price' : obj.price,
            }
            lines.append(vals)
        return lines    
    

