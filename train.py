import csv
from sklearn import svm
import sklearn.ensemble
import time
from sklearn import linear_model
# import sklearn.linear_model

start_time = time.clock()

def getXy(list_of_days, down_sample=37):
    X = []
    y = []
        
    for day in list_of_days:
        reader_feature = csv.reader(file('output/features_%d.csv' % day, 'r'))
        reader_result = csv.reader(file('output/y_%d.csv' % day, 'r'))

        count = 0
        for feature, result in zip(reader_feature, reader_result):
            result = int(result[2])
            
            if result == 0:
                count += 1
                if count % down_sample == 0:
                    X.append(feature[2:])
                    y.append(result)
            else:
                X.append(feature[2:])
                y.append(result)
    return X, y

X, y = getXy([1218, 1208, 1204, 1123], 30)
# X, y = getXy([1218], 30)



# clf =svm.SVC(kernel='rbf', C=1, gamma=13)
clf =svm.SVC(kernel='rbf', C=3.2, gamma=0.60)
# clf = svm.SVC(kernel='rbf', C=2.1, gamma=0.07)
# clf = svm.SVC(kernel='linear')
clf.fit(X, y)
# clf = sklearn.ensemble.RandomForestClassifier(200)
# clf.fit(X, y)

reader_feature = csv.reader(file('output/features_1217.csv', 'rb'))
reader_result = csv.reader(file('output/y_1217.csv', 'rb'))

X = []
y = []
for (a, b) in zip(reader_feature, reader_result):
    X.append(a[2:])
    y.append(int(b[2]))


predict = clf.predict(X)


true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

real_buy = csv.reader(file('output/real_buy_1217.csv', 'r'))
buy_set = set()
for row in real_buy:
    buy_set.add(tuple(row))
reader_result = csv.reader(file('output/y_1217.csv', 'r'))
result_set = set()
for result, row in zip(predict, reader_result):
    if result:
        result_set.add(tuple([row[0], row[1]]))
    
        
true_positive = len(set.intersection(buy_set, result_set))
false_positive = len(result_set) - true_positive
false_negative = len(buy_set) - true_positive
print true_positive, false_positive, false_negative, true_negative 
precision = float(true_positive) / (true_positive + false_positive)
recall = float(true_positive) / (true_positive + false_negative)
f1 = 2 / (1 / precision + 1 / recall)
print precision, recall, f1



X = []
reader = csv.reader(file('output/features_1219.csv', 'r'))
for row in reader:
    X.append(row[2:])
  
predict = clf.predict(X)
  
writer = csv.writer(file('output/tianchi_mobile_recommendation_predict.csv', 'w'))
reader = csv.reader(file('output/features_1219.csv', 'r'))
    
writer.writerow(['user_id', 'item_id'])
for (x, y) in zip(reader, predict):
    if int(y) == 1:
        writer.writerow([str(x[0]), str(x[1])])
  
stop_time = time.clock()
print stop_time - start_time
