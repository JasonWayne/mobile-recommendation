import csv
import MySQLdb

con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = con.cursor()

# data = csv.reader(file('output/tianchi_mobile_recommendation_predict.csv', 'r'))
# data = csv.reader(file('tianchi_mobile_recommendation_predict.csv', 'r'))
data = csv.reader(file('final.csv', 'r'))

first_line = True 
filtered_data = []
for row in data:
    has_geo = False
    if first_line:
        first_line = False
        continue
    user_id = row[0]
    item_id = row[1]
    # find (u, i) which both have geo information
    sql_item = """SELECT item_id, item_geohash FROM items WHERE item_id = %d""" % int(item_id)
    cursor.execute(sql_item)
    item_geo = ''
    for row_item in cursor:
        if len(row_item[1]):
            has_geo = True
            item_geo = row_item[1]

    if has_geo:
        sql_user = """SELECT user_id, item_id, user_geohash FROM users WHERE user_id=%d and item_id = %d""" % (int(user_id), int(item_id))
        cursor.execute(sql_user)
        no_delete = True
        for row1 in cursor:
            if len(row1[2]):
                user_geo = row1[2]
                if item_geo[0] != user_geo[0] or item_geo[1] != user_geo[1]:
                    no_delete = False 
        if no_delete:
            filtered_data.append(row)
            continue
        else:
            print row[0], row[1]
            continue
    
    filtered_data.append(row)
    
writer = csv.writer(file('tianchi_filtered.csv', 'w'))
writer.writerow(['user_id', 'item_id'])
for row in filtered_data:
    writer.writerow(row)
                
