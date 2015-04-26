# encoding: utf-8

import MySQLdb
import csv
import time

start = time.clock()

csv_data = csv.reader(file('original/tianchi_mobile_recommend_train_item.csv'))
# csv_data = csv.reader(file('original/tianchi_mobile_recommend_train_user.csv'))
# errors = csv.writer(file('error_items.csv', 'wb'))
# csv_data = csv.reader(file('output/user_51816656.txt', 'r'))

INSERT_INTO_ITEM_TABLE = "INSERT INTO items (item_id, item_geohash, item_category) \
        VALUES (%s, %s, %s)"

INSERT_INTO_USER_TABLE = "INSERT INTO users (user_id, item_id, behavior_type, \
        user_geohash, item_category, time) \
        VALUES (%s, %s, %s, %s, %s, %s)"
        
INSERT_INTO_USER518_TABLE = "INSERT INTO user_518 (user_id, item_id, behavior_type, \
        user_geohash, item_category, time) \
        VALUES (%d, %d, %d, '%s', %d, '%s')"

db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()

count = 0
data = []
for row in csv_data:
    if count == 0:
        count = 1
        continue
#     row = tuple([int(row[0]), int(row[1]), int(row[2]), str(row[3]), int(row[4]), str(row[5])])
    row = tuple([int(row[0]), str(row[1]), int(row[2])])
    data.append(row)
    count += 1
    if count % 1000 == 0:

        print 'INSERT %dth row' % count
#         py = INSERT_INTO_USER_TABLE 
        sql = INSERT_INTO_ITEM_TABLE
        cursor.executemany(sql, data)
        db.commit()
        data = []
else:
    cursor.executemany(sql, data)
    db.commit()
   
print count
     
db.close()

end = time.clock()
print end - start