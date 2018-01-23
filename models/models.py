from odoo import api, models, fields, http
from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
import xmlrpclib

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
		# table = self.env['product.attribute.value.product.product.rel']
		# for record in self:
		# 	db_object = table.search([('product_product_id', '=', record.product_id.id)])
		# 	self.product_attribute_value_id = db_object.product_attribute_value_id
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

	@api.one
	def download_xlsx(self, cr, uid, ids, context={}): 
		context = context or {}
		host = 'http://localhost:8069'
		database = 'invendb11_clone'
		username = 'user@test.com'
		password = 'test1234'

		common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %host)
		user_id = common.authenticate(database, username, password, {})
		odoo_api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %host)

		records = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_read', [[]], {'fields':['product_template_id', 'product_template_id_name', 'product_attribute_id','product_attribute_id_name', 'product_category_id', 'product_category_id_name', 'product_attribute_value_id', 'product_attribute_value_id_name', 'qty'] })

		workbook = xlsxwriter.Workbook('Current Inventory.xlsx')
		worksheet = workbook.add_worksheet()

		# Formatting variant data
		prodIdRecords = []

		for record in (records):
			if not record['product_template_id'] in prodIdRecords:
				prodIdRecords.append(record['product_template_id'])

		# Formatting expected data 
		expectedOutput = []

		for prodId in (prodIdRecords):
			tempArray = []
			i = 0
			for record in (records):	
				if prodId == record['product_template_id']:
					if i == 0:
						tempArray.append(record['product_category_id_name'])
						tempArray.append(record['product_template_id_name'])
						i+=1
					tempArray.append(record['product_attribute_id_name'])
					tempArray.append(record['product_attribute_value_id_name'])
					tempArray.append(record['qty'])
			expectedOutput.append(tempArray)

		print expectedOutput

		# Write data in file

		row = 1
		col = 0

		worksheet.write(0, 0, 'Category')
		worksheet.write(0, 1, 'Product')

		inc = 2
		for i in range(0,9):
			worksheet.write(0, inc, 'Variant')
			worksheet.write(0, inc + 1, 'Attribute')
			worksheet.write(0, inc + 2, 'Qty')
			inc += 3

		# Iterate over the data and write it out row by row.
		for item in (expectedOutput):
			counter = 0
			for i in range(0,len(item)):
				worksheet.write(row, counter, item[counter])
				counter += 1
			row += 1

		workbook.close()
		print("Done")



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