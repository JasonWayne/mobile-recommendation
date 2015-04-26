import MySQLdb
import csv
from constants import TimeUtil


CREATE_TABLE_USERS_FILETERED = """CREATE TABLE users_filtered FROM (SELECT * FROM users WHERE item_id IN (SELECT DISTINCT(item_id) FROM items))"""

GET_BASE_SQL = '''SELECT user_id, item_id FROM users_filtered 
WHERE behavior_type = 3
and time >= '2014-12-%s %d' 
and time <= '2014-12-%s 24' 
and (user_id, item_id) NOT IN 
    (SELECT user_id, item_id FROM users_filtered 
    WHERE behavior_type = 4 
    and time >= '2014-12-%s' 
    and time <= '2014-12-%s 24')
GROUP BY user_id, item_id
'''

def get_base(yesterday, hour):
    con = MySQLdb.connect("localhost", "root", '', 'mobile_recommendation')
    cursor = con.cursor()
    start_day = int(yesterday)
    start_day = to_str(start_day)
    cursor.execute(GET_BASE_SQL % tuple([start_day, hour, yesterday, start_day, yesterday]))
#     writer = csv.writer(file('test/12%s%d_collect.csv' % (yesterday, hour), 'w'))
    writer = csv.writer(file('new_train/base.csv', 'w'))
    writer.writerow(['user_id', 'item_id'])
    for row in cursor:
        writer.writerow([str(row[0]), str(row[1])])
        
def calculate_f1(predict_day, yesterday, hour):
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    
    real_buy = csv.reader(file('output/real_buy_12%s.csv' % predict_day, 'r'))
    buy_set = set()
    for row in real_buy:
        buy_set.add(tuple(row))
#     reader_result = csv.reader(file('test/12%s%d_2.csv' % (yesterday, hour), 'r'))
    reader_result = csv.reader(file('test/12%s%d_collect.csv' % (yesterday, hour), 'r'))
    result_set = set()
    for row in reader_result:
        result_set.add(tuple(row))
            
    true_positive = len(set.intersection(buy_set, result_set))
    false_positive = len(result_set) - true_positive
    false_negative = len(buy_set) - true_positive
    print true_positive, false_positive, false_negative, true_negative 
    precision = float(true_positive) / (true_positive + false_positive)
    recall = float(true_positive) / (true_positive + false_negative)
    f1 = 2 / (1 / precision + 1 / recall)
    return precision, recall, f1
        
def to_str(cart_day):
    if cart_day >= 1 and cart_day < 10:
        cart_day = '0' + str(cart_day)
    else:
        cart_day = str(cart_day)
    return cart_day

def geo_filter(yesterday, hour):
    con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
    cursor = con.cursor()
    
    # data = csv.reader(file('output/tianchi_mobile_recommendation_predict.csv', 'r'))
    data = csv.reader(file('test/12%s%d_collect.csv' % (yesterday, hour), 'r'))
    
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
        
        writer = csv.writer(file('test/filtered_12%s%d.csv' % (yesterday, hour), 'w'))
        writer.writerow(['user_id', 'item_id'])
        for row in filtered_data:
            writer.writerow(row)

if __name__ == '__main__':
#     hour = 22
#     for i in range(1, 18):
#         i = to_str(i)
#         get_base(i, hour)
#     writer = csv.writer(file('test/score_2%d.csv' % hour, 'w'))
#     for i in range(2, 19):
#         yesterday = i - 1
#         i = to_str(i)
#         yesterday = to_str(yesterday)
#         row = calculate_f1(i, yesterday, hour)
#         row = ['%.3f' % row[0], '%.3f' % row[1], '%.3f' % row[2]]
#         writer.writerow([i, row])
#     for i in range(1, 18):
#         i = to_str(i)
#         geo_filter(i, hour)
#     writer = csv.writer(file('test/score_%d_filtered.csv' % hour, 'w'))
#     for i in range(2, 19):
#         yesterday = i - 1
#         i = to_str(i)
#         yesterday = to_str(yesterday)
#         row = calculate_f1(i, yesterday, hour)
#         row = ['%.3f' % row[0], '%.3f' % row[1], '%.3f' % row[2]]
#         writer.writerow([i, row])
    get_base(18, 20)
        