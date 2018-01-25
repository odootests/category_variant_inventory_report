import psycopg2, xlsxwriter

connection = psycopg2.connect(database="invendb11_clone_2", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
print "Connection with DB Established"

cursor = connection.cursor()

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
print "Fetched Records"

for row in records:
	print row

workbook = xlsxwriter.Workbook('CurrentInventory.xlsx')
worksheet = workbook.add_worksheet()
print "WorkBook Initialized"

prodIdRecords = []
for record in (records):
	#record[1] = product_template_id
	if not record[1] in prodIdRecords:
		prodIdRecords.append(record[1])

print "Indexing Product IDs"
print prodIdRecords

variantNameRecords = []
for record in (records):
	#record[8] = product_attribute_value_name
	if not record[8] in variantNameRecords:
		variantNameRecords.append(record[8])

print "Indexing Variant ID Names"
print variantNameRecords

expectedOutput = []

for prodId in (prodIdRecords):
	tempArray = []
	i = 0
	for variantName in variantNameRecords:
		j=0
		for record in (records):
			#record[1] = product_template_id	
			if prodId == record[1]:
				if i == 0:
					#record[6] = product_category_name
					tempArray.append(record[6])
					#record[2] = product_template_name
					tempArray.append(record[2])
					i+=1
			
				if variantName == record[8]:
					#record[9] = actual_qty
					tempArray.append(record[9])
				else:
					if j==0:
						# tempArray.append('X')
						j+=1
	expectedOutput.append(tempArray)

expectedOutput2 = []

for prodId in (prodIdRecords):
	tempArray2 = []
	i = 0
	for record in (records):
		#record[1] = product_template_id	
		if prodId == record[1]:
			if i == 0:
				#record[6] = product_category_name
				tempArray2.append(record[6])
				#record[2] = product_template_name
				tempArray2.append(record[2])
				i+=1
			for name in variantNameRecords:
				if not record[8] == name:
					tempArray2.append(0)
					continue
				else:
					tempArray2.append(record[9])
	expectedOutput2.append(tempArray2)

print "Data after Loop"
print expectedOutput2

# print expectedOutput

print "Start Arrangement"

worksheet.write(0, 0, 'Category')
worksheet.write(0, 1, 'Product')

inc=2
count = 0

for item in variantNameRecords:
	worksheet.write(0, inc+count, item)
	count+=1

row = 1
col = 0

# for item in (expectedOutput):
for item in (expectedOutput2):
	counter = 0
	# print item[1]
	for i in range(0,len(item)):
		# print item[i]
		worksheet.write(row, counter, item[counter])
		counter += 1
	row += 1

workbook.close()
print "Closing Workbook"

connection.close()
print "Connection Closed"
