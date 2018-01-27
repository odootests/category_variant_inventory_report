from odoo import http
import xlsxwriter, datetime

class InventoryReport(http.Controller):
	@http.route('/inventory/current', website='True')
	def index(self, **kw):
		stock_quant = http.request.env['stock.inventory.line']
		current_stock = stock_quant.search([])
		context = {
			'current_stock': current_stock
		}
		return http.request.render('ilyn_inven_report_v2.show_current_stock', context)

	@http.route('/inventory/current/now', auth='user', website='True')
	def current_inventory(self, **kw):
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

		current_timestamp = datetime.datetime.now()

		workbook = xlsxwriter.Workbook('CurrentInventory.xlsx')
		worksheet = workbook.add_worksheet()
		
		worksheet.write(0, 0, 'Category')
		worksheet.write(0, 1, 'Product')

		inc=2
		count = 0

		for item in variantNameRecords:
			worksheet.write(0, inc+count, item)
			count+=1

		row = 1
		col = 0

		for item in (expectedOutput):
			counter = 0
			# print item[1]
			for i in range(0,len(item)):
				# print item[i]
				worksheet.write(row, counter, item[counter])
				counter += 1
			row += 1

		workbook.close()

		context = {
			'current_timestamp': current_timestamp,
			'variantNameRecords': variantNameRecords,
			'expectedOutput': expectedOutput,
		}
		return http.request.render('ilyn_inven_report_v2.inventory_current_stock', context)