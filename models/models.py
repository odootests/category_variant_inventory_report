from odoo import api, models, fields, http

class InventoryReports(models.Model):
	_inherit='stock.quant'
	product_template_id = fields.Integer(compute='get_product_template_id', store=True)
	product_template_id_name = fields.Char(compute='get_product_template_id_name', store=True)
	product_attribute_id = fields.Integer(compute='get_product_attribute_id', store=True)
	product_attribute_id_name = fields.Char(compute='get_product_attribute_id_name', store=True)
	product_category_id = fields.Integer(compute='get_product_category_id', store=True)
	product_category_id_name = fields.Char(compute='get_product_category_id_name', store=True)
	product_attribute_value_id = fields.Integer(compute='get_product_attribute_value_id', store=True)
	product_attribute_value_id_name = fields.Char(compute='get_product_attribute_value_id_name', store=True)
	actual_qty = fields.Integer(compute='calc_product_actual_qty', store=True)

	# @api.one
	@api.depends('product_id')
	def get_product_template_id(self):
		self.env.cr.execute("SELECT product_tmpl_id FROM product_product WHERE id=%s", [(self.product_id.id)])
		self.product_template_id = self.env.cr.fetchone()[0]
	
	@api.depends('product_template_id')
	def get_product_template_id_name(self):
		table = self.env['product.template']
		for record in self:
			db_object = table.search([('id', '=', record.product_template_id )])
			self.product_template_id_name = db_object.name

	@api.depends('product_template_id')
	def get_product_attribute_id(self):
		table = self.env['product.attribute.line']
		for record in self:
			db_object = table.search([('product_tmpl_id', '=', record.product_template_id)])
			self.product_attribute_id = db_object.attribute_id

	@api.depends('product_attribute_id')
	def get_product_attribute_id_name(self):
		table =  self.env['product.attribute']
		for record in self:
			db_object = table.search([('id', '=', record.product_attribute_id)])
			self.product_attribute_id_name = db_object.name

	@api.depends('product_attribute_id')
	def get_product_attribute_value_id(self):
		self.env.cr.execute("SELECT product_attribute_value_id FROM product_attribute_value_product_product_rel WHERE product_product_id=%s", [(self.product_id.id)])
		self.product_attribute_value_id = self.env.cr.fetchone()[0]

	@api.depends('product_attribute_id')
	def get_product_attribute_value_id_name(self):
		table = self.env['product.attribute.value']
		for record in self:
			db_object = table.search([('id', '=', record.product_attribute_value_id)])
			self.product_attribute_value_id_name  = db_object.name

	@api.depends('product_template_id')
	def get_product_category_id(self):
		table = self.env['product.template']
		for record in self:
			db_object = table.search([('id', '=', record.product_template_id)])
			self.product_category_id = db_object.categ_id

	@api.depends('product_category_id')
	def get_product_category_id_name(self):
		table = self.env['product.category']
		for record in self:
			db_object = table.search([('id', '=', record.product_category_id)])
			self.product_category_id_name  = db_object.name

	@api.depends('product_id')
	def calc_product_actual_qty(self):
		self.env.cr.execute("SELECT currentTable.product_id, currentTable.product_qty, newTable.create_date from (SELECT product_id, MAX(create_date) AS create_date FROM stock_inventory_line GROUP BY product_id) AS newTable INNER JOIN stock_inventory_line AS currentTable ON newTable.product_id = currentTable.product_id AND newTable.create_date = currentTable.create_date;")
		results = self.env.cr.fetchall()
		for record in results:
			if record[0] == self.product_id.id:
				self.actual_qty = record[1]
