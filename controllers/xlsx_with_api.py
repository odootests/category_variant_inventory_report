import xlsxwriter
import xmlrpclib, csv

host = 'http://localhost:8069'
database = 'invendb11'
username = 'user@test.com'
password = 'test1234'

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %host)
user_id = common.authenticate(database, username, password, {})
odoo_api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %host)

records = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_read', [[]], {'fields':['product_template_id', 'product_template_id_name', 'product_attribute_id','product_attribute_id_name', 'product_category_id', 'product_category_id_name', 'product_attribute_value_id', 'product_attribute_value_id_name', 'qty'] })

workbook = xlsxwriter.Workbook('MyXLS.xlsx')
worksheet = workbook.add_worksheet()

# Formatting variant data
prodVariantRecords = [];

new_array = [];
for record in (records):
	new_array = [record['product_template_id'], record['product_template_id_name'], record['product_attribute_id_name'], record['product_attribute_value_id_name'], record['qty']]
	prodVariantRecords.append(record['product_category_id_name'])

print prodVariantRecords

# Formatting expected data
expectedOutput = [];

for record in (records):
	new_array = [record['product_category_id_name'], record['product_template_id_name'], record['product_attribute_id_name'], record['product_attribute_value_id_name'], record['qty']]
	expectedOutput.append(new_array)

print expectedOutput

# Start from the first cell. Rows and columns are zero indexed.

# Initialize column name 
worksheet.write(0, 0, 'Category')
worksheet.write(0, 1, 'Product')
worksheet.write(0, 2, 'Variant')
worksheet.write(0, 3, 'Attribute')
worksheet.write(0, 4, 'Qty')

row = 1
col = 0

# Iterate over the data and write it out row by row.
for item in (expectedOutput):
	worksheet.write(row, col, item[0])
	worksheet.write(row, col + 1, item[1])
	worksheet.write(row, col + 2, item[2])
	worksheet.write(row, col + 3, item[3])
	worksheet.write(row, col + 4, item[4])
	row += 1

# Write a total using a formula.
# worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B5)')

workbook.close()
print("Success")