from odoo import api, models, fields, http

class InventoryReports(models.Model):
	_inherit='stock.quant'
	product_template_id = fields.Integer(compute='get_product_template_id', store=True)
	product_template_id_name = fields.Char(compute='get_product_template_id_name', store=True)
	product_attribute_id = fields.Integer(compute='get_product_attribute_id', store=True)
	product_attribute_id_name = fields.Char(compute='get_product_attribute_id_name', store=True)
	product_attribute_value_id = fields.Integer(compute='get_product_attribute_value_id', store=True)
	product_attribute_value_id_name = fields.Char(compute='get_product_attribute_value_id_name', store=True)

	# @api.one
	@api.depends('product_id')
	def get_product_template_id(self):
		self.env.cr.execute("SELECT product_tmpl_id FROM product_product WHERE id=%s", [(self.product_id.id)])
		self.product_template_id = self.env.cr.fetchone()[0]
	
	@api.depends('product_template_id')
	def get_product_template_id_name(self):
		product_template_table = self.env['product.template']
		for record in self:
			product_template_id_name_obj = product_template_table.search([('id', '=', record.product_template_id )])
			self.product_template_id_name = product_template_id_name_obj.name

	@api.depends('product_template_id')
	def get_product_attribute_id(self):
		product_attribute_line_table = self.env['product.attribute.line']
		for record in self:
			product_attribute_line_obj = product_attribute_line_table.search([('product_tmpl_id', '=', record.product_template_id)])
			self.product_attribute_id = product_attribute_line_obj.attribute_id

	@api.depends('product_attribute_id')
	def get_product_attribute_id_name(self):
		product_attribute_table =  self.env['product.attribute']
		for record in self:
			product_attribute_line_name_obj = product_attribute_table.search([('id', '=', record.product_attribute_id)])
			self.product_attribute_id_name = product_attribute_line_name_obj.name

	@api.depends('product_attribute_id')
	def get_product_attribute_value_id(self):
		product_attribute_value_table = self.env['product.attribute.value']
		for record in self:
			product_attribute_value_id_obj = product_attribute_value_table.search([('id', '=', record.product_attribute_id)])
			self.product_attribute_value_id = product_attribute_value_id_obj.id

	@api.depends('product_attribute_id')
	def get_product_attribute_value_id_name(self):
		product_attribute_value_table = self.env['product.attribute.value']
		for record in self:
			product_attribute_value_id_obj = product_attribute_value_table.search([('id', '=', record.product_attribute_id)])
			self.product_attribute_value_id_name  = product_attribute_value_id_obj.name


	# @api.one
	# @api.depends('product_attribute_line_id')
	# def get_product_attribute_value(self):
	# 	product_attribute_val = self.env['product.attribute.value']
	#    for record in self:
	#       the_product_attribute_line_val = product_attribute_val.search([('product_tmpl_id','=', 2)])
	#       self.product_attribute_line_id = the_product_attribute_line_id.id



	# warehouse_id = fields.Integer(compute='get_warehouse_id')
	
	# def get_warehouse_id(self):
	#    stock_warehouse = self.env['stock.warehouse']
	#    for record in self:
	#       the_warehouse_id = stock_warehouse.search([('lot_stock_id', '=', 15)])  
	#       for whid in the_warehouse_id:
	#          self.warehouse_id = the_warehouse_id.id
	#       #self.warehouse_name = the_warehouse_id.name