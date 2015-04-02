import MySQLdb
import csv

writer = csv.writer(file("output/user518_bought_item_related_behavoir.txt", "wb"))

db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()

sql = """SELECT * FROM user_518 WHERE item_id in
            (SELECT item_id FROM user_518 WHERE behavior_type = 4) ORDER BY time"""
    
cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    writer.writerow(row)

db.close()
            
