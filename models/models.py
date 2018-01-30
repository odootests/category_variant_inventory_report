from odoo import api, models, fields

class InventoryReports(models.Model):
	_inherit='stock.inventory.line'
	product_template_id = fields.Integer(compute='get_product_template_id', store=True)
	product_template_name = fields.Char(compute='get_product_template_name', store=True)
	product_attribute_id = fields.Integer(compute='get_product_attribute_id', store=True)
	product_attribute_name = fields.Char(compute='get_product_attribute_name', store=True)
	product_category_id = fields.Integer(compute='get_product_category_id', store=True)
	product_category_name = fields.Char(compute='get_product_category_name', store=True)
	product_category_fullname = fields.Char(compute='get_product_category_fullname', store=True)
	product_attribute_value_id = fields.Integer(compute='get_product_attribute_value_id', store=True)
	product_attribute_value_name = fields.Char(compute='get_product_attribute_value_name', store=True)
	actual_qty = fields.Integer(compute='calc_product_actual_qty', store=True)

	@api.one
	@api.depends('product_id')
	def get_product_template_id(self):
		table = self.env['product.product']
		for record in self:
			db_object = table.search([('id', '=', record.product_id.id)])
			self.product_template_id = db_object.product_tmpl_id

	@api.one
	@api.depends('product_template_id')
	def get_product_template_name(self):
		table = self.env['product.template']
		for record in self:
			db_object = table.search([('id', '=', record.product_template_id )])
			self.product_template_name = db_object.name

	@api.one
	@api.depends('product_template_id')
	def get_product_attribute_id(self):
		table = self.env['product.attribute.line']
		for record in self:
			db_object = table.search([('product_tmpl_id', '=', record.product_template_id)])
			self.product_attribute_id = db_object.attribute_id

	@api.one
	@api.depends('product_attribute_id')
	def get_product_attribute_name(self):
		table =  self.env['product.attribute']
		for record in self:
			db_object = table.search([('id', '=', record.product_attribute_id)])
			self.product_attribute_name = db_object.name

	@api.one
	@api.depends('product_id')
	def get_product_attribute_value_id(self):
		# table = self.env['product.attribute.value.product.product.rel']
		for record in self:
			# db_object = table.search(['product_product_id', '=', record.product_id.id])
			self.env.cr.execute("SELECT product_attribute_value_id FROM product_attribute_value_product_product_rel WHERE product_product_id=%s", [(record.product_id.id)])
		# results = self.env.cr.fetchall()
		# for record in results:
			self.product_attribute_value_id = self.env.cr.fetchone()[0]
			#self.product_attribute_value_id = db_object.product_attribute_value_id

	@api.one
	@api.depends('product_attribute_id')
	def get_product_attribute_value_name(self):
		table = self.env['product.attribute.value']
		for record in self:
			db_object = table.search([('id', '=', record.product_attribute_value_id)])
			self.product_attribute_value_name  = db_object.name

	@api.one
	@api.depends('product_template_id')
	def get_product_category_id(self):
		table = self.env['product.template']
		for record in self:
			db_object = table.search([('id', '=', record.product_template_id)])
			self.product_category_id = db_object.categ_id

	@api.one
	@api.depends('product_category_id')
	def get_product_category_name(self):
		table = self.env['product.category']
		for record in self:
			db_object = table.search([('id', '=', record.product_category_id)])
			self.product_category_name  = db_object.name

	@api.one
	@api.depends('product_category_id')
	def get_product_category_fullname(self):
		table = self.env['product.category']
		num_rows = table.search_count([])
		for record in self:
			db_object = table.search([('id', '=', record.product_category_id)])
			temp_cat_name = []
			for i in range(0,num_rows):
				if db_object.parent_id:
					temp_cat_name.append(db_object.name)
					new_catID = db_object.parent_id.id
					db_object = table.search([('id', '=', new_catID)])
				if not db_object.parent_id:
					temp_cat_name.append(db_object.name)
					break
			temp_cat_name.reverse()
			temp_cat_name = ' / '.join(temp_cat_name)
			self.product_category_fullname = temp_cat_name
	
	@api.one
	@api.depends('product_id')
	def calc_product_actual_qty(self):
		self.env.cr.execute("SELECT currentTable.product_id, currentTable.product_qty from (SELECT product_id, MAX(create_date) AS create_date FROM stock_inventory_line GROUP BY product_id) AS newTable INNER JOIN stock_inventory_line AS currentTable ON newTable.product_id = currentTable.product_id AND newTable.create_date = currentTable.create_date;")
		results = self.env.cr.fetchall()
		for record in results:
			if record[0] == self.product_id.id:
				self.actual_qty = record[1]
