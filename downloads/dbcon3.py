import psycopg2

connection = psycopg2.connect(database="report_test_j29", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
print "Connection with DB Established"
cursor = connection.cursor()

cursor.execute("SELECT COUNT(id) FROM product_category;")
num_rows = cursor.fetchall()[0]
print("Num rows: %s" %num_rows)

cursor.execute("SELECT id,parent_id,name FROM product_category;")
records = cursor.fetchall()
temp_cat_name = []
for record in records:
	print "ID: %s \tPARENT_ID: %s \t NAME: %s" %(record[0],record[1],record[2])
	db_object = record[0]
	for i in range (0, num_rows):
		if record[1]:
			temp_cat_name.append(record[2])


