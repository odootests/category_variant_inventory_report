from odoo import http

class InventoryReport(http.Controller):
   @http.route('/inventory/current')
   def index(self, **kw):
      return "Hey"
