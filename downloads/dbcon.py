import psycopg2, xlsxwriter

connection = psycopg2.connect(database="invendb11_clone_2", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
print "Connection with DB Established"

cursor = connection.cursor()
cursor.execute("SELECT product_id, product_template_id, product_template_name, product_attribute_id, product_attribute_name, product_category_id, product_category_name, product_attribute_value_id, product_attribute_value_name, actual_qty FROM stock_inventory_line")
records_old = cursor.fetchall()
# for row in records:
# 	print row
print "Fetched Records"

cursor.execute('''SELECT 
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
records = cursor.fetchall()

workbook = xlsxwriter.Workbook('CurrentInventory.xlsx')
worksheet = workbook.add_worksheet()
print "WorkBook Initialized"

prodIdRecords = []
for record in (records):
	#record[1] = product_template_id
	if not record[1] in prodIdRecords:
		prodIdRecords.append(record[1])

variantIdRecords = []
for record in (records):
	#record[8] = product_attribute_value_name
	if not record[8] in variantIdRecords:
		variantIdRecords.append(record[8])

expectedOutput = []

for prodId in (prodIdRecords):
	tempArray = []
	i = 0
	for record in (records):
		#record[1] = product_template_id	
		if prodId == record[1]:
			if i == 0:
				#record[6] = product_category_name
				tempArray.append(record[6])
				#record[2] = product_template_name
				tempArray.append(record[2])
				i+=1
				# for item in variantIdRecords:
			#record[9] = actual_qty
			tempArray.append(record[9])
	expectedOutput.append(tempArray)

print expectedOutput

row = 1
col = 0

worksheet.write(0, 0, 'Category')
worksheet.write(0, 1, 'Product')

inc=2
count = 0

for item in variantIdRecords:
	worksheet.write(0, inc+count, item)
	count+=1

# Iterate over the data and write it out row by row.
for item in (expectedOutput):
	counter = 0
	for i in range(0,len(item)):
		worksheet.write(row, counter, item[counter])
		counter += 1
	row += 1

workbook.close()
print "Workbook Complete"

connection.close()
print "Connection Closed"
