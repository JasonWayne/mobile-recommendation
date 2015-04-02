# encoding: utf-8

import MySQLdb
import csv

# csv_data = csv.reader(file('tianchi_mobile_recommend_train_item.csv'))
# csv_data = csv.reader(file('tianchi_mobile_recommend_train_user.csv'))
# errors = csv.writer(file('error_items.csv', 'wb'))
csv_data = csv.reader(file('output/user_51816656.txt', 'r'))

INSERT_INTO_ITEM_TABLE = "INSERT INTO items (item_id, item_geohash, item_category) \
        VALUES (%d, '%s', %d)"

INSERT_INTO_USER_TABLE = "INSERT INTO users (user_id, item_id, behavior_type, \
        user_geohash, item_category, time) \
        VALUES (%d, %d, %d, '%s', %d, '%s')"
        
INSERT_INTO_USER518_TABLE = "INSERT INTO user_518 (user_id, item_id, behavior_type, \
        user_geohash, item_category, time) \
        VALUES (%d, %d, %d, '%s', %d, '%s')"

db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()

count = 0
for row in csv_data:
#     if count == 0:
#         count = 1
#         continue
   
    sql = INSERT_INTO_USER518_TABLE % (int(row[0]), int(row[1]), int(row[2]), 
                                    str(row[3]), int(row[4]), str(row[5]))
    cursor.execute(sql)
    db.commit()
   
print count
     
db.close()

