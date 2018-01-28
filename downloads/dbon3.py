import psycopg2

connection = psycopg2.connect(database="report_test", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
print "Connection with DB Established"

cursor = connection.cursor()
cursor.execute('''SELECT id,parent_id,name FROM product_category;''')
results = cursor.fetchall()
print "Fetched Records"

for row in records:
	print row

