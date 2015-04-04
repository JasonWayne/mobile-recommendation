import MySQLdb
import csv

con = MySQLdb.connect('localhost', 'root','', 'mobile_recommendation')
cursor = con.cursor()

sql = """SELECT item_id, COUNT(*) FROM users_filtered WHERE behavior_type = 4 GROUP BY item_id"""
cursor.execute(sql)

data = []
for row in cursor:
    data.append(list(row))

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

    
writer = csv.writer(file('output/item_total_bought.csv', 'w'))
for row in data:
    writer.writerow(row)

print (0-mean)/std

