from odoo import http

class InventoryReport(http.Controller):
   @http.route('/inventory/current')
   def index(self, **kw):
      stock_quant = http.request.env['stock.quant.cust']
      current_stock = stock_quant.search([])
      first_record = current_stock[0]
      context = {
      	'first_record': first_record,
         'current_stock': current_stock
      }
      return http.request.render('ilyn_inven_report_v2.show_current_stock', context)
