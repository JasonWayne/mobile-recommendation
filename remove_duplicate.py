import csv

reader = csv.reader(file('new_train/base.csv', 'r'))
writer = csv.writer(file('new_train/filtered.csv', 'w'))

writer.writerow(['user_id', 'item_id'])

s = set()
for row in reader:
    s.add(tuple(row))
    
for item in s:
    writer.writerow(item)
