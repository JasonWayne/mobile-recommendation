import MySQLdb
import time
import csv

output = csv.writer(file("output/users_filtered.csv", 'wb'))
db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()
# sql = """SELECT * FROM users WHERE user_id = 51816656"""
sql = """SELECT * FROM users_filtered"""


start_time = time.clock()
cursor.execute(sql)
for row in cursor:
    output.writerow(row)
    
time_used = time.clock() - start_time
print time_used

db.close()