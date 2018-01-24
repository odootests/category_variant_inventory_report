import psycopg2, xlsxwriter

connection = psycopg2.connect(database="invendb11_clone_2", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
print "Connection with DB Established"

cursor = connection.cursor()
cursor.execute("SELECT product_id, product_template_id, product_template_id_name, product_attribute_id, product_attribute_id_name, product_category_id, product_category_id_name, product_attribute_value_id, product_attribute_value_id_name, actual_qty FROM stock_quant")
records = cursor.fetchall()
print "Fetched Records"

workbook = xlsxwriter.Workbook('CurrentInventory.xlsx')
worksheet = workbook.add_worksheet()
print "WorkBook Initialized"

prodIdRecords = []
for record in (records):
	if not record[1] in prodIdRecords:
		prodIdRecords.append(record[1])

variantIdRecords = []
for record in (records):
	if not record[8] in variantIdRecords:
		variantIdRecords.append(record[8])

connection.close()
print "Connection Closed"
