import csv
import time
from constants import *
import numpy as np
import MySQLdb

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
        input_path = 'output/features_%d.csv' % self.predict_day
        reader = csv.reader(file(input_path, 'r'))
        writer = csv.writer(file('output/y_%d.csv' % self.predict_day, 'wb'))
         
        for row in reader:
            if tuple([row[0], row[1]]) in self.true_buy_set:
                row.append(1)
            else:
                row.append(0)
            writer.writerow([row[0], row[1], row[-1]])
        
        
class FeatureGetter():
    def __init__(self, predict_day):
        self.predict_day = predict_day
        self.data = []
        self.original_path = 'output/users_filtered.csv'
        
    def append_four_features(self, row, new_row):
        # click
        if int(row[COLUMN_BEHAVIOR]) == 1:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # collect
        if int(row[COLUMN_BEHAVIOR]) == 2:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # add to cart
        if int(row[COLUMN_BEHAVIOR]) == 3:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # buy
        if int(row[COLUMN_BEHAVIOR]) == 4:
            new_row.append(1)
        else:
            new_row.append(0)
        
    def mapper(self):
        print time.ctime() + " --> mapper()"
        original = csv.reader(file(self.original_path, 'r'))
        count = 0
        for row in original:
            if count == 0:
                count = 1
                continue
            
            count += 1
#             if count % 1000 == 0:
#                 print "do with %d's line" % count
            
            if TimeUtil.format_date(row[5]) > (self.predict_day - 1) or TimeUtil.format_date(row[5]) < (self.predict_day - 2):
                continue
            
#             if TimeUtil.format_date(row[5]) == (self.predict_day - 3) and TimeUtil.format_hour(row[5]) <= 12:
#                 continue
#             
            new_row = [int(row[0]), int(row[1])] 
    
            # add features of seven days behavior
            self.append_four_features(row, new_row)
                
            # add features of last day behavior
            if TimeUtil.format_date(row[5]) == (self.predict_day - 1):
                self.append_four_features(row, new_row)
            else:
                new_row.extend([0,0,0,0])

            # add features of last half day behavior
            if TimeUtil.format_date(row[5]) == (self.predict_day - 1) and TimeUtil.format_hour(row[5]) >= 12: 
                self.append_four_features(row, new_row)
            else:
                new_row.extend([0,0,0,0])
                
            calcvalue = TimeUtil.calc_interval(self.predict_day, row[5])
            new_row.append(calcvalue)

            self.data.append(new_row)

    def add_two_row(self, r1, r2):
        to = 14
        for i in range(2, to):
            r1[i] = str(int(r1[i]) + int(r2[i]))
        r1[to] = min(r1[to], r2[to])
        return r1
    
    def sort(self):
        print time.ctime() + " --> sort()"
        self.data = sorted(self.data)
    
    def reducer(self):
        print time.ctime() + " --> reducer()"
        reduced = []

        first_line = True
        for row in self.data:
            if first_line:
                previous_row = row
                first_line = False
                continue
            
            if previous_row[0] == row[0] and previous_row[1] == row[1]:
                previous_row = self.add_two_row(previous_row, row)
            else:
                reduced.append(previous_row)
                previous_row = row
        else:
            reduced.append(previous_row)
        
        self.data = reduced
    
    def add_item_last_days_interact(self, days):
        data = []
        fun = None
        if days == 15:
            fun = TimeUtil.fifteen_days_before
        elif days == 7:
            fun = TimeUtil.seven_days_before
        else:
            fun = TimeUtil.three_days_before
        con = MySQLdb.connect('localhost', 'root','', 'mobile_recommendation')
        cursor = con.cursor()
        sql = "SELECT DISTINCT(item_id), COUNT(*) FROM users_filtered WHERE \
                 time > '%s' and time < '%s' GROUP BY item_id;" % (TimeUtil.get_day_str(fun(self.predict_day)), TimeUtil.get_day_str(self.predict_day))
        cursor.execute(sql)
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)

        
        d = {}
        for row in data:
            d[row[0]] = row[1]
#         print d
        for row in self.data:
            if d.get(int(row[1])):
                row.append(d.get(int(row[1])))
            else:
                row.append(0)
                
        cursor.close()
        con.close()
    
    def add_item_last_days_buy(self, days):
        data = []
        fun = None
        if days == 15:
            fun = TimeUtil.fifteen_days_before
        elif days == 7:
            fun = TimeUtil.seven_days_before
        else:
            fun = TimeUtil.three_days_before
        con = MySQLdb.connect('localhost', 'root','', 'mobile_recommendation')
        cursor = con.cursor()
        sql = "SELECT DISTINCT(item_id), COUNT(*) FROM users_filtered WHERE behavior_type = 4 AND \
                 time > '%s' and time < '%s' GROUP BY item_id;" % (TimeUtil.get_day_str(fun(self.predict_day)), TimeUtil.get_day_str(self.predict_day))
        cursor.execute(sql)
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)

        
        d = {}
        for row in data:
            d[row[0]] = row[1]
#         print d
        for row in self.data:
            if d.get(int(row[1])):
                row.append(d.get(int(row[1])))
            else:
                row.append(0)
                
        cursor.close()
        con.close()

    def add_item_feature(self):
        print time.ctime() + ' --> add_item_feature()'
        # get last 7 days bought information
        self.add_item_last_days_buy(15)
        self.add_item_last_days_buy(7)
        self.add_item_last_days_buy(3)
        # of no use
        self.add_item_last_days_interact(15)
        self.add_item_last_days_interact(7)
        self.add_item_last_days_interact(3)

                
    def get_user_data_from_db(self, behavior_type):
        data = []
        con = MySQLdb.connect("localhost", 'root', '', 'mobile_recommendation')
        cursor = con.cursor()
        sql = "SELECT user_id, count(*) FROM users_filtered WHERE behavior_type = %d and \
                time < '%s%%' \
                 GROUP BY user_id" % (behavior_type, TimeUtil.get_day_str(self.predict_day))
        cursor.execute(sql)
        con.close()
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)
        
        d = {}
        for row in data:
            d[int(row[0])] = row[1]
        return d
    
    def append_row(self, d, default_value):
        for row in self.data:
            if d.get(int(row[0])):
                row.append(d.get(int(row[0])))
            else:
                row.append(default_value)
                
    def add_user_last_days_buy(self, days):
        data = []
        con = MySQLdb.connect("localhost", 'root', '', 'mobile_recommendation')
        cursor = con.cursor()
        fun = None
        if days == 15:
            fun = TimeUtil.fifteen_days_before
        elif days == 7:
            fun = TimeUtil.seven_days_before
        else:
            fun = TimeUtil.three_days_before
        sql = "SELECT DISTINCT(user_id), COUNT(*) FROM users_filtered WHERE behavior_type = 4 AND \
                 time > '%s' and time < '%s' GROUP BY user_id;" % (TimeUtil.get_day_str(fun(self.predict_day)), TimeUtil.get_day_str(self.predict_day))
        cursor.execute(sql)
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)
            
        d = {}
        for row in data:
            d[row[0]] = row[1]
#         print d
        for row in self.data:
            if d.get(int(row[0])):
                row.append(d.get(int(row[0])))
            else:
                row.append(0)
                 
        cursor.execute(sql)
        con.close()
    
    def add_user_last_days_interact(self, days):
        data = []
        con = MySQLdb.connect("localhost", 'root', '', 'mobile_recommendation')
        cursor = con.cursor()
        fun = None
        if days == 15:
            fun = TimeUtil.fifteen_days_before
        elif days == 7:
            fun = TimeUtil.seven_days_before
        else:
            fun = TimeUtil.three_days_before
        sql = "SELECT DISTINCT(user_id), COUNT(*) FROM users_filtered WHERE \
                 time > '%s' and time < '%s' GROUP BY user_id;" % (TimeUtil.get_day_str(fun(self.predict_day)), TimeUtil.get_day_str(self.predict_day))
        cursor.execute(sql)
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)
            
        d = {}
        for row in data:
            d[row[0]] = row[1]
#         print d
        for row in self.data:
            if d.get(int(row[0])):
                row.append(d.get(int(row[0])))
            else:
                row.append(0)
                 
        cursor.execute(sql)
        con.close()

            
    def add_user_feature(self):
        print time.ctime() + " --> add_user_feature() "
        self.add_user_last_days_buy(15)
        self.add_user_last_days_buy(7)
        self.add_user_last_days_buy(3)
        self.add_user_last_days_interact(15)
        self.add_user_last_days_interact(7)
        self.add_user_last_days_interact(3)
    
    def output(self):
        print time.ctime() + " --> output()"
        output_path = 'output/features_%d.csv' % self.predict_day
        writer = csv.writer(file(output_path, 'wb'))
        for e in self.data:
            writer.writerow(e)
    
    def get_features(self):
        self.mapper()
        self.sort()
        self.reducer()
#         self.normalize()
        self.add_item_feature()
        self.add_user_feature()
        self.output()
        
def train(day):
    getter = FeatureGetter(day)
    getter.get_features()
    resultGetter = ResultsGetter(day)
    resultGetter.get_result()
    

def format_features():
    start = time.clock()
#     train(1218)
#     train(1217)
    train(1216)
    train(1215)

    train(1208)
    train(1209)
#     train(1206)
#     train(1205)
#     train(1204)
    train(1130)
#     train(1129)
#     train(1128)
#     train(1127)

#     train(1122)

    end = time.clock()
    print end-start

def submit():
    getter = FeatureGetter(1219)
    getter.get_features()

if __name__ == "__main__":
#     format_features()
    submit()



        
    

    