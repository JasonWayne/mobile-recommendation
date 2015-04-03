import MySQLdb
import time
import csv

db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()
# output = csv.writer(file("output/users_filtered.csv", 'wb'))
# sql = """SELECT * FROM users_filtered"""

output = csv.writer(file('output/user-35254700.csv', 'wb'))
sql = """SELECT * FROM users WHERE user_id = 35254700"""

start_time = time.clock()
cursor.execute(sql)
for row in cursor:
    output.writerow(row)
    
time_used = time.clock() - start_time
print time_used

db.close()