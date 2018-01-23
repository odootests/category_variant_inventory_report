import xmlrpclib, csv

host = 'http://localhost:8069'
database = 'invendb11'
username = 'user@test.com'
password = 'test1234'

common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' %host)
user_id = common.authenticate(database, username, password, {})
odoo_api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' %host)

product_ids = odoo_api.execute_kw(database, user_id, password, 'stock.quant', 'search_read', [[]], {'fields':['product_id'] })

productIDs = []
for record in product_ids:
	if not record['product_id'] in productIDs:
		productIDs.append(record['product_id'])
		print record['product_id']

filter_by_stockquant_prod_id = [[('product_tmpl_id', '=', temp_prod_id)]]
product_template_id = odoo_api.execute_kw(database, user_id, password, 'product.product', 'search', filter_by_stockquant_prod_id)
