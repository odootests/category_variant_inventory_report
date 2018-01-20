from odoo import api, models, fields, http

class InventoryReports(models.Model):
   _inherit='stock.quant'
   product_template_id = fields.Many2one(related='product_id.product_tmpl_id')
   

   # warehouse_id = fields.Integer(compute='get_warehouse_id')
   
   # def get_warehouse_id(self):
   #    stock_warehouse = self.env['stock.warehouse']
   #    for record in self:
   #       the_warehouse_id = stock_warehouse.search([('lot_stock_id', '=', 15)])  
   #       for whid in the_warehouse_id:
   #          self.warehouse_id = the_warehouse_id.id
   #       #self.warehouse_name = the_warehouse_id.name