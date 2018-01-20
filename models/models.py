from odoo import api, models, fields

class InventoryReports(models.Model):
   _inherit='stock.quant'
   product_template_id = fields.Many2one(related='product_id.product_tmpl_id')
   
   # def get_product_template_id(self):
   #    for rec in self:
   #       self.product_template_id = self.product_id.product_tmpl_id
