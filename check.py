import csv

reader = csv.reader(file('output/submit.txt', 'rb'))

for row in reader:
    previous = row