import csv
import time
from constants import *
import numpy as np
import MySQLdb

class TimeUtil():
    @staticmethod
    def format_date(s):
        return int(s[5:7] + s[8:10])
    
    @staticmethod
    def format_hour(s):
        return int(s[11:13])
    
    @staticmethod
    def calc_interval(predict_day, s):
        behavior_date = TimeUtil.format_date(s)
        behavior_hour = TimeUtil.format_hour(s)
        if predict_day / 100 == 12 and behavior_date / 100 == 11:
            predict_day += 30
        predict_day %= 100
        behavior_date %= 100
        day_interval = predict_day - behavior_date
        
        return day_interval * 24 - behavior_hour 

    @staticmethod
    def get_last_seven_days_str(predict_day):
        #example return input: 1128, output: ['2014-11-21', '2014-11-22', ... , '2014-11-27']
        yesterday = TimeUtil.yesterday(predict_day)
        l = []
        for i in range(7):
            month = yesterday / 100
            day = yesterday % 100
            l.append('2014-%d-%d' % (month, day))
            yesterday = TimeUtil.yesterday(yesterday)
        return l
    
    @staticmethod
    def yesterday(day):
        '''input: 1201
            output:1130
            designed for dates between 20141119 - 20141220
        '''
        return day - 1 if day != 1201 else 1130
        
        
        
             

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
            
            if TimeUtil.format_date(row[5]) > (self.predict_day - 1) or TimeUtil.format_date(row[5]) < (self.predict_day - 3):
                continue
            
            new_row = [int(row[0]), int(row[1])] 
    
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
        for i in range(2, 14):
            r1[i] = str(int(r1[i]) + int(r2[i]))
        r1[14] = max(r1[14], r2[14])
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
        
    def normalize_column(self, column_number):
        total = 0
        line_count = 0
        max_val = 0
        for row in self.data:
            if int(row[column_number]) > max_val:
                max_val = int(row[column_number])
            total += int(row[column_number])
            line_count += 1
        mean = float(total) / line_count
        
        total = 0
        for row in self.data:
            total += (float(row[column_number]) - mean) ** 2
        std = total / line_count
        
        for row in self.data:
            row[column_number] = (float(row[column_number]) - mean) / std
            
    
    def normalize(self):
        self.normalize_column(2)
        self.normalize_column(6)
        self.normalize_column(10)
        self.normalize_column(14)

    def add_item_feature(self):
        # get last 7 days bought information
        con = MySQLdb.connect('localhost', 'root','', 'mobile_recommendation')
        cursor = con.cursor()
        data = []
        
        dates = TimeUtil.get_last_seven_days_str(self.predict_day)
        sql = "SELECT item_id, COUNT(*) FROM users_filtered WHERE behavior_type = 4 AND \
            (time LIKE '%s%%'   \
            or time LIKE '%s%%' \
            or time LIKE '%s%%' \
            or time LIKE '%s%%' \
            or time LIKE '%s%%' \
            or time LIKE '%s%%' \
            or time LIKE '%s%%') \
            GROUP BY item_id" % tuple(dates)
        cursor.execute(sql)
        
        for row in cursor:
            row = list(row)
            row[0] = int(row[0])
            data.append(row)
        
        total = 0
        line_count = 0
        max_val = 0
        for row in data:
            if int(row[1]) > max_val:
                max_val = int(row[1])
            total += int(row[1])
            line_count += 1
        mean = float(total) / line_count
        
        total = 0
        for row in data:
            total += (float(row[1]) - mean) ** 2
        std = total / line_count
        
        for row in data:
            row[1] = (float(row[1]) - mean) / std

        d = {}
        for row in data:
            d[row[0]] = row[1]
#         print d
        for row in self.data:
            if d.get(int(row[1])):
                row.append(d.get(int(row[1])))
            else:
#                 row.append((0-mean) / std)
                row.append(-1)
    
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
        self.normalize()
        self.add_item_feature()
        self.output()
        
def train(day):
    getter = FeatureGetter(day)
    getter.get_features()
    resultGetter = ResultsGetter(day)
    resultGetter.get_result()
    

def format_features():
    start = time.clock()
    train(1218)
    train(1208)
    train(1204)
    train(1123)

    train(1217)
    end = time.clock()
    print end-start

def submit():
    getter = FeatureGetter(1219)
    getter.get_features()

format_features()
submit()



        
    

    