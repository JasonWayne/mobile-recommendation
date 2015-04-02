import csv
from sklearn import svm
import sklearn.ensemble
import time
# import sklearn.linear_model

start_time = time.clock()

reader = csv.reader(file('output/train.csv', 'r'))

X = []
count = 0
for row in reader:
    if int(row[6]) == 0:
        count += 1
        if count % 450 == 0:
            X.append(row[2:6])
    else:
        X.append(row[2:6])
    
y = []
reader = csv.reader(file('output/train.csv', 'r'))
count = 0
for row in reader:
    if int(row[6]) == 0:
        count += 1
        if count % 450 == 0:
            y.append(row[6])
    else:
        y.append(int(row[6]))


    
clf = svm.SVC(kernel='rbf', C=1)
clf.fit(X, y)
# clf = sklearn.ensemble.RandomForestClassifier(1000)
# clf.fit(X, y)

reader = csv.reader(file('output/normalized_1216_1218.csv', 'rb'))
X = []
for row in reader:
    X.append(row[2:6])

predict = clf.predict(X)

reader = csv.reader(file('output/normalized_1216_1218.csv', 'rb'))
writer = csv.writer(file('output/tianchi_mobile_recommendation_predict.csv', 'wb'))

writer.writerow(['user_id', 'item_id'])
for (x, y) in zip(reader, predict):
    if int(y) == 1:
        writer.writerow([x[0], x[1]])

# true_positive = 0
# false_positive = 0
# true_negative = 0
# false_negative = 0
# total = 0
# 
# for (x, y) in zip(predict, y):
#     print x,y
#     total += 1
#     x = int(x)
#     y = int(y)
#     if x == 1 and y == 1:
#         true_positive += 1
#     elif x == 1 and y == 0:
#         false_positive += 1
#     elif x == 0 and y == 1:
#         false_negative += 1
#     elif x == 0 and y == 0:
#         true_negative += 1
#     
#         
# print total, true_positive, false_positive, false_negative, true_negative 
# precision = float(true_positive) / (true_positive + false_positive)
# print precision 

stop_time = time.clock()
print stop_time - start_time
        
