import xlsxwriter
import xmlrpclib, csv

host = 'http://localhost:8069'
database = 'invendb11_clone'
username = 'user@test.com'
password = 'test1234'

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %host)
user_id = common.authenticate(database, username, password, {})
odoo_api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %host)

records = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_read', [[]], {'fields':['product_template_id', 'product_template_id_name', 'product_attribute_id','product_attribute_id_name', 'product_category_id', 'product_category_id_name', 'product_attribute_value_id', 'product_attribute_value_id_name', 'qty'] })

workbook = xlsxwriter.Workbook('CurrentInventory.xlsx')
worksheet = workbook.add_worksheet()

# Formatting variant data
prodIdRecords = []

for record in (records):
	if not record['product_template_id'] in prodIdRecords:
		prodIdRecords.append(record['product_template_id'])

variantIdRecords = []
for record in (records):
	if not record['product_attribute_value_id_name'] in variantIdRecords:
		variantIdRecords.append(record['product_attribute_value_id_name'])

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
			# tempArray.append(record['product_attribute_value_id_name'])
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