from odoo import http
import datetime
from time import strftime, gmtime

class InventoryReport(http.Controller):
	@http.route('/inventory/test')
	def test(self, **kw):
		table = http.request.env['product.category']
		db_object = table.search([('id', '=', 6)])
		num_rows = table.search_count([])
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

		product_category_fullname = temp_cat_name
		num_rows = table.search_count([])
		context = {
			# 'temp_cat_name':temp_cat_name,
			'product_category_fullname':product_category_fullname,
			'num_rows':num_rows
		}
		return http.request.render('ilyn_inven_report_v2.test', context)


	@http.route('/inventory/current/raw', website='True')
	def index(self, **kw):
		stock_quant = http.request.env['stock.inventory.line']
		current_stock = stock_quant.search([])
		context = {
			'real_date' : datetime.datetime.now(),
			'current_stock': current_stock
		}
		return http.request.render('ilyn_inven_report_v2.show_current_stock', context)

	@http.route('/inventory/current/', auth='user', website='True')
	def current_inventory(self, **kw):
		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_template_id=(SELECT product_tmpl_id FROM product_product WHERE id=(product_id)) WHERE product_template_id is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_template_name=(SELECT name FROM product_template WHERE id=(product_template_id)) WHERE product_template_name is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_attribute_id=(SELECT attribute_id FROM product_attribute_line WHERE product_tmpl_id=(product_template_id)) WHERE product_attribute_id is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_attribute_name=(SELECT name FROM product_attribute WHERE id=(product_attribute_id)) WHERE product_attribute_name is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_category_id=(SELECT categ_id FROM product_template WHERE id=(product_template_id)) WHERE product_category_id is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_category_name=(SELECT name FROM product_category WHERE id=(product_category_id)) WHERE product_category_name is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_attribute_value_id=(SELECT product_attribute_value_id FROM product_attribute_value_product_product_rel WHERE product_product_id=(product_id)) WHERE product_attribute_value_id is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET product_attribute_value_name=(SELECT name FROM product_attribute_value WHERE id=(product_attribute_value_id)) WHERE product_attribute_value_name is null;")

		http.request.env.cr.execute("UPDATE public.stock_inventory_line SET actual_qty=(select currentTable.product_qty from (select product_id, MAX(create_date) as create_date from stock_inventory_line group by product_id) as newTable Inner JOIN stock_inventory_line as currentTable ON newTable.product_id = currentTable.product_id AND newTable.create_date = currentTable.create_date WHERE newTable.product_id =(stock_inventory_line.product_id)) where actual_qty is null;")

		http.request.env.cr.execute('''SELECT 
			currentTable.product_id, 
			currentTable.product_template_id, 
			currentTable.product_template_name, 
			currentTable.product_attribute_id, 
			currentTable.product_attribute_name, 
			currentTable.product_category_id, 
			currentTable.product_category_name, 
			currentTable.product_attribute_value_id, 
			currentTable.product_attribute_value_name, 
			currentTable.actual_qty FROM
				(SELECT product_id, MAX(create_date) AS create_date FROM stock_inventory_line GROUP BY product_id) AS newTable INNER JOIN stock_inventory_line AS currentTable ON newTable.product_id = currentTable.product_id AND newTable.create_date = currentTable.create_date ORDER BY product_template_name, product_attribute_value_name;''')
		current_stock = http.request.env.cr.dictfetchall()

		prodIdRecords = []
		for record in (current_stock):
			#record[1] = product_template_id
			if not record['product_template_id'] in prodIdRecords:
				prodIdRecords.append(record['product_template_id'])

		variantIdRecords = []
		for record in (current_stock):
			#record[7] = product_attribute_value_id
			if not record['product_attribute_value_id'] in variantIdRecords:
				variantIdRecords.append(record['product_attribute_value_id'])

		variantNameRecords = []
		for record in (current_stock):
			#record[8] = product_attribute_value_name
			if not record['product_attribute_value_name'] in variantNameRecords:
				variantNameRecords.append(record['product_attribute_value_name'])

		expectedOutput = []

		for prodId in (prodIdRecords):
			tempArray = []
			i = 0

			for record in (current_stock):
				#record[1] = product_template_id	
				if prodId == record['product_template_id']:
					if i == 0:
						#record[6] = product_category_name
						tempArray.append(record['product_category_name'])
						#record[2] = product_template_name
						tempArray.append(record['product_template_name'])
						i+=1
				
			for variantId in (variantIdRecords):
				findVariant = False	
				tempVariantIdRecords = []		
				counter=0	
				for record in (current_stock):
					#record[1] = product_template_id	
					#record[7] = product_attribute_value_id
					if prodId == record['product_template_id'] and not variantId in tempVariantIdRecords and variantId == record['product_attribute_value_id']:
						#record[9] = actual_qty
						tempArray.append(record['actual_qty'])
						tempVariantIdRecords.append(variantId)
						findVariant = True
					counter+=1	
				if findVariant == False and counter == len(current_stock):
					tempArray.append('0')
					
			expectedOutput.append(tempArray)

		current_date = datetime.datetime.now()
		current_date = strftime("%a, %d-%m-%Y")

		context = {
			'current_date': current_date,
			'variantNameRecords': variantNameRecords,
			'expectedOutput': expectedOutput,
		}
		return http.request.render('ilyn_inven_report_v2.inventory_current_stock', context)