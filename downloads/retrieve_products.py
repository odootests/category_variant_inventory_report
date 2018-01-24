import xmlrpclib, csv
# Create a workbook and add a worksheet.

host = 'http://localhost:8069'
database = 'invendb11'
username = 'user@test.com'
password = 'test1234'

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %host)
#print common.version()

user_id = common.authenticate(database, username, password, {})
odoo_api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %host)

stock_quant_count = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_count', [[]])
#print('No. Rows in Table: %s' %stock_quant_count)

records = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_read', [[]], {'fields':['product_template_id', 'product_template_name', 'product_attribute_id','product_attribute_name', 'product_category_id', 'product_category_name', 'product_attribute_value_id', 'product_attribute_value_name', 'qty'] })

for record in records:
	#print record['product_attribute_name']
   for field in record:
   	print field, record[field]


#for key in all_stock:
#	print key, all_stock[key]