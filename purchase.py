# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import pytz
import math

from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class purchase_order(osv.osv):
	_name = 'purchase.order'
	_inherit = 'purchase.order'

	_columns = {
                'deffective_ids': fields.one2many('purchase.order.deffectives','order_id','Deffective Products'),
                }



purchase_order()


class purchase_order_deffectives(osv.osv):
        _name = 'purchase.order.deffectives'
        _description = 'Deffective Products POs'

        _columns = {
                'order_id': fields.many2one('purchase.order','Pedido'),
                'product_id': fields.many2one('product.product','Producto'),
                'isbn': fields.related('product_id','ean13',type="char",string="ISBN"),
                'default_code': fields.related('product_id','default_code',type="char",string="UBS Code"),
                'qty': fields.integer('Quantity'),
                }


        def _check_product(self, cr, uid, ids, context=None):
        	obj = self.browse(cr, uid, ids[0], context=context)
		po_product_ids = []
		return_value = False
		for line in obj.order_id.order_line:
			if obj.product_id.id == line.product_id.id and obj.qty <= line.product_qty:
				return_value = True
				break
        	return return_value

	_constraints = [
		(_check_product, 'Product needs to be included in PO and its qty should be lower than the ordered qty',['product_id','qty']),
		]


purchase_order_deffectives()


