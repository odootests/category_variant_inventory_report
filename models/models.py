from odoo import api, models, fields, http

class InventoryReports(models.Model):
	_inherit='stock.quant'
	name='stock.quant.cust'
	product_template_id = fields.Integer(compute='get_product_template_id', store=True)

	@api.one
	@api.depends('product_id')
	def get_product_template_id(self):
		product_product_table = self.env['product.product']
		for record in self:
			product_template_id_obj = product_product_table.search([('product_tmpl_id', '=', record.product_id.id )])
			self.product_template_id = product_template_id_obj.id