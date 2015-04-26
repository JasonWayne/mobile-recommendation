import MySQLdb
import csv

sql = '''SELECT * FROM users_filtered 
WHERE behavior_type = 3
and time >= '2014-12-18 20' 
and time <= '2014-12-18 24' 
and (user_id, item_id) NOT IN 
    (SELECT user_id, item_id FROM users_filtered 
    WHERE behavior_type = 4 
    and time >= '2014-12-11'
    and time <= '2014-12-18 24')
GROUP BY user_id, item_id
'''


con = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = con.cursor()
cursor.execute(sql)

count = 0
writer = csv.writer(file('base.csv', 'w'))
for row in cursor: 
    writer.writerow(row)
    count += 1
    
print count
cursor.close()
con.close()
    
