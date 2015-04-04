import MySQLdb
import csv

def get_buy_in_1217():
    con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
    cursor = con.cursor()
    sql = """SELECT user_id, item_id FROM users_filtered WHERE time LIKE '2014-12-17%' and behavior_type = 4"""
    writer = csv.writer(file("output/real_buy_1217.csv", 'wb')) 
    cursor.execute(sql)
    count = 0
    for row in cursor:
        count += 1
        writer.writerow(row)
    print count

get_buy_in_1217()
        