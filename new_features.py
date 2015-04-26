import csv
import MySQLdb
from constants import TimeUtil
import time

start = time.clock()

class ResultsGetter():
    def __init__(self, predict_day):
        self.predict_day = predict_day
        self.true_buy_set = set() 

    def get_result(self):
        print time.ctime() + " --> get_result()"
        reader = csv.reader(file('output/users_filtered.csv', 'r'))
        for row in reader:
            if TimeUtil.format_date(row[5]) == self.predict_day and int(row[2]) == 4:
                self.true_buy_set.add(tuple([row[0], row[1]]))
        input_path = 'new_train/features_%d.csv' % self.predict_day
        reader = csv.reader(file(input_path, 'r'))
        writer = csv.writer(file('new_train/y_%d.csv' % self.predict_day, 'wb'))
         
        for row in reader:
            print row
            if tuple([row[0], row[1]]) in self.true_buy_set:
                row.append(1)
            else:
                row.append(0)
            writer.writerow([row[0], row[1], row[-1]])

def get_base(day_str):
    GET_BASE_SQL = '''SELECT user_id, item_id FROM users_filtered 
    WHERE behavior_type = 3
    and time >= '%s 07' 
    and time <= '%s 24' 
    and (user_id, item_id) NOT IN 
        (SELECT user_id, item_id FROM users_filtered 
        WHERE behavior_type = 4 
        and time >= '%s' 
        and time <= '%s 24')
    GROUP BY user_id, item_id
    '''
    writer = csv.writer(file('new_train/%s_cart.csv' % day_str, 'w'))
    con = MySQLdb.connect("localhost", 'root', '', 'mobile_recommendation')
    cursor = con.cursor()
    cursor.execute(GET_BASE_SQL % (day_str, day_str, day_str, day_str))
    for row in cursor:
        writer.writerow(row)
    cursor.close()
    con.close()

def select_feature(sql):
    con = MySQLdb.connect("localhost", 'root', '', 'mobile_recommendation')
    cursor = con.cursor()
    cursor.execute(sql)
    ret = 0
    a = cursor.fetchone()
    if a:
        ret = 1
    cursor.close()
    con.close()
    return ret

if __name__ == '__main__':
    cart_day = 1218
    predict_day = cart_day + 1
    day_str = TimeUtil.get_day_str(cart_day)
    yesterday_str = TimeUtil.yesterday_str(day_str)
    get_base(day_str)
    reader = csv.reader(file('new_train/%s_cart.csv' % day_str, 'r'))
    count = 0
    total = 0
    writer = csv.writer(file('new_train/features_%d.csv' % predict_day, 'w'))
    for row in reader:
        user_id = row[0]
        item_id = row[1]
          
        # feature 1 - add to cart after 12 o'clock
        sql = '''SELECT 1 FROM users_filtered 
                WHERE user_id = %s and item_id = %s and behavior_type = 3
                and time >= '%s 12' 
                and time <= '%s 24' 
                GROUP BY user_id, item_id
                ''' % (user_id, item_id, day_str, day_str)
        row.append(select_feature(sql))
   
        # feature 2 - add to cart after 20 o'clock
        sql = '''SELECT 1 FROM users_filtered 
                WHERE user_id = %s and item_id = %s and behavior_type = 3
                and time >= '%s 20' 
                and time <= '%s 24' 
                GROUP BY user_id, item_id
                ''' % (user_id, item_id, day_str, day_str)
        row.append(select_feature(sql))
            
        # feature 3 - add to cart after 22 o'clock
        sql = '''SELECT 1 FROM users_filtered 
                WHERE user_id = %s and item_id = %s and behavior_type = 3
                and time >= '%s 22' 
                and time <= '%s 24' 
                GROUP BY user_id, item_id
                ''' % (user_id, item_id, day_str, day_str)
        if select_feature(sql):
            total += 1
        row.append(select_feature(sql))
           
        # feature 4 - collect
        sql = '''SELECT 1 FROM users_filtered 
                WHERE user_id = %s and item_id = %s and behavior_type = 2
                and time >= '%s' 
                and time <= '%s 24' 
                GROUP BY user_id, item_id
                ''' % (user_id, item_id, yesterday_str, day_str)
        row.append(select_feature(sql))
  
           
        # feature 5 - user if buy today, add to cart yesterday
    
        temp_day = cart_day
    
        while temp_day > 1118:
            temp_day_str = TimeUtil.get_day_str(temp_day)
            temp_yesterday_str = TimeUtil.yesterday_str(temp_day_str)
            sql = '''SELECT 1 FROM users_filtered 
                WHERE behavior_type = 3
                and time >= '%s'
                and time <= '%s 24' 
                and user_id = '%s'
                and (user_id, item_id) IN 
                    (SELECT user_id, item_id FROM users_filtered 
                    WHERE behavior_type = 4 
                    and time >= '%s' 
                    and time <= '%s 24')
                GROUP BY user_id
                '''
            sql = sql % (temp_yesterday_str, temp_yesterday_str, user_id, temp_day_str, temp_day_str)
            if select_feature(sql):
                row.append(1)
                break
            temp_day = TimeUtil.yesterday(temp_day)
        else:
            row.append(0)
  
        # feature 6 - user if buy today, collect yesterday in history
        temp_day = cart_day
    
        while temp_day > 1118:
            temp_day_str = TimeUtil.get_day_str(temp_day)
            temp_yesterday_str = TimeUtil.yesterday_str(temp_day_str)
            sql = '''SELECT 1 FROM users_filtered 
                WHERE behavior_type = 2
                and time >= '%s'
                and time <= '%s 24' 
                and user_id = '%s'
                and (user_id, item_id) IN 
                    (SELECT user_id, item_id FROM users_filtered 
                    WHERE behavior_type = 4 
                    and time >= '%s' 
                    and time <= '%s 24')
                GROUP BY user_id
                '''
            sql = sql % (temp_yesterday_str, temp_yesterday_str, user_id, temp_day_str, temp_day_str)
            if select_feature(sql):
                row.append(1)
                break
            temp_day = TimeUtil.yesterday(temp_day)
        else:
            row.append(0)
  
        # feature 7 - user if buy in history
        sql = '''SELECT 1 FROM users_filtered 
               WHERE behavior_type = 4
               and user_id = '%s'
               and time < '%s 24'
               '''
        sql = sql % (user_id, day_str)
        if select_feature(sql):
            row.append(1)
        else:
            row.append(0)
  
        # feature 8 - item if buy in history
        sql = """SELECT 1 FROM users_filtered
                WHERE behavior_type = 4
                and item_id = %s
                and time < '%s 24'
                """
        sql = sql % (item_id, day_str)
        if select_feature(sql):
            row.append(1)
        else:
            row.append(0)
          
        writer.writerow(row)
        
        
#     # get result
#     resultGetter = ResultsGetter(predict_day)
#     resultGetter.get_result()
    
#     print total

    
end = time.clock()
print end - start