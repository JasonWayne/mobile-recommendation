from __builtin__ import staticmethod
USER_ID = 0
ITEM_ID = 1
FEATURE_TWO_DAY_CLICK = 2
FEATURE_TWO_DAY_COLLECT = 3
FEATURE_TWO_DAY_CART = 4
FEATURE_TWO_DAY_BUY = 5
FEATURE_ONE_DAY_CLICK = 6
FEATURE_ONE_DAY_COLLECT = 7
FEATURE_ONE_DAY_CART = 8
FEATURE_ONE_DAY_BUY = 9
FEATURE_HALF_DAY_CLICK = 10
FEATURE_HALF_DAY_COLLECT = 11
FEATURE_HALF_DAY_CART = 12
FEATURE_HALF_DAY_BUY = 13
FEATURE_LAST_INTERACT_TIME = 14
FEATURE_ITEM_LAST_15_DAY_BUY = 15
FEATURE_ITEM_LAST_7_DAY_BUY = 16
FEATURE_ITEM_LAST_3_DAY_BUY = 17
FEATURE_ITEM_LAST_15_DAY_INTERACT = 18
FEATURE_ITEM_LAST_7_DAY_INTERACT = 19
FEATURE_ITEM_LAST_3_DAY_INTERACT = 20
FEATURE_USER_LAST_15_DAY_BUY = 21
FEATURE_USER_LAST_7_DAY_BUY = 22
FEATURE_USER_LAST_3_DAY_BUY = 23
# 30 days feature
FEATURE_USER_BUY_CLICK_RATIO = 17
FEATURE_USER_BUY_COLLECT_RATIO = 18
FEATURE_USER_BUY_CART_RATIO = 19

COLUMN_USER_ID = 0
COLUMN_ITEM_ID = 1
COLUMN_BEHAVIOR = 2
COLUMN_GEOHASH = 3
COLUMN_ITEM_CATEGORY = 4
COLUMN_TIME = 5

# Fridays
# 1121, 1128, 1205

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
    def get_last_five_days_str(predict_day):
        #example return input: 1128, output: ['2014-11-25', '2014-11-26', '2014-11-27']
        yesterday = TimeUtil.yesterday(predict_day)
        l = []
        for _ in range(5):
            month = yesterday / 100
            cart_day = yesterday % 100
            l.append('2014-%d-%d' % (month, cart_day))
            yesterday = TimeUtil.yesterday(yesterday)
        return l
    
    @staticmethod
    def get_day_str(predict_day):
        month = str(predict_day / 100)

        cart_day = str(predict_day % 100) if predict_day % 100 >= 10 else '0' + str(predict_day % 100)

        return '2014-%s-%s' % (month, cart_day)
    
    @staticmethod
    def yesterday(cart_day):
        '''input: 1201
            output:1130
            designed for dates between 20141119 - 20141220
        '''
        return cart_day - 1 if cart_day != 1201 else 1130
    
    @staticmethod
    def yesterday_str(day_str):
        today = TimeUtil.format_date(day_str)
        yesterday = TimeUtil.yesterday(today)
        return TimeUtil.get_day_str(yesterday)
    
    @staticmethod
    def seven_days_before(cart_day):
        for _ in range(7):
            cart_day = TimeUtil.yesterday(cart_day)
        return cart_day
    
    @staticmethod
    def fifteen_days_before(cart_day):
        for _ in range(15):
            cart_day = TimeUtil.yesterday(cart_day)
        return cart_day
    
    @staticmethod
    def three_days_before(cart_day):
        for _ in range(3):
            cart_day = TimeUtil.yesterday(cart_day)
        return cart_day