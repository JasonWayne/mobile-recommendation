import MySQLdb
import csv
from prepare_data import TimeUtil

def get_buy_result(predict_day):
    day = TimeUtil.get_day_str(predict_day)
    con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
    cursor = con.cursor()
    sql = "SELECT user_id, item_id FROM users_filtered WHERE time LIKE '%s%%' and behavior_type = 4" % day
    writer = csv.writer(file("output/real_buy_%d.csv" % predict_day, 'wb')) 
    cursor.execute(sql)
    count = 0
    for row in cursor:
        count += 1
        writer.writerow(row)
    print count

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

def get_buy_in_1218():
    con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
    cursor = con.cursor()
    sql = """SELECT user_id, item_id FROM users_filtered WHERE time LIKE '2014-12-18%' and behavior_type = 4"""
    writer = csv.writer(file("output/real_buy_1218.csv", 'wb')) 
    cursor.execute(sql)
    count = 0
    for row in cursor:
        count += 1
        writer.writerow(row)
    print count
    
def get_buy_in_1205():
    con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
    cursor = con.cursor()
    sql = """SELECT user_id, item_id FROM users_filtered WHERE time LIKE '2014-12-05%' and behavior_type = 4"""
    writer = csv.writer(file("output/real_buy_1205.csv", 'wb')) 
    cursor.execute(sql)
    count = 0
    for row in cursor:
        count += 1
        writer.writerow(row)
    print count

def all_result():
    for day in range(1122, 1131) + range(1201, 1219):
        get_buy_result(day)

all_result()