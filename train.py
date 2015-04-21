import csv
from sklearn import svm
import sklearn.ensemble
import time
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.learning_curve import learning_curve
import matplotlib.pyplot as plt

start_time = time.clock()

def getXy(list_of_days, down_sample=37):
    X = []
    y = []
        
    for day in list_of_days:
        reader_feature = csv.reader(file('output/features_%d.csv' % day, 'r'))
        reader_result = csv.reader(file('output/y_%d.csv' % day, 'r'))

        count = 0
        count_pos = 0
        count_neg = 0
        total = 0
        for feature, result in zip(reader_feature, reader_result):
            total += 1
            feature[2:] = map(lambda x: float(x), feature[2:])
            result = int(result[2])
            
            if result == 0:
                count += 1
                if count % down_sample == 0:
                    X.append(feature[2:])
                    y.append(result)
                    count_neg += 1
            else:
                X.append(feature[2:])
                y.append(result)
                count_pos += 1
        print count_pos, count_neg, total
    return X, y

# X, y = getXy([1217, 1208, 1204, 1123], 60)
# X, y = getXy([1218], 27)
X, y = getXy([1218, 1208, 1127,1129,1204, 1205], 27)
scalar = StandardScaler()
X = scalar.fit_transform(X)
# train_sizes , train_scores, validation_scores = learning_curve(linear_model.LogisticRegression(), X, y, train_sizes=[x for x in range(100, 5000, 200)], cv=5)
# plt.plot(train_sizes, train_scores, 'r')
# plt.plot(train_sizes, validation_scores, 'b')
# plt.show()


# clf = svm.SVC(kernel='rbf', C=2.3, gamma=0.55)
# clf =svm.SVC(kernel='rbf', C=1, gamma=13)
# clf =svm.SVC(kernel='rbf', C=3.1, gamma=0.6)
# clf = svm.SVC(kernel='rbf', C=2.1, gamma=0.07)
# clf = svm.SVC(kernel='rbf', C=30, gamma=0.2)
# clf = svm.SVC()
# clf = svm.SVC(kernel='linear')
clf = linear_model.LogisticRegression(C=1)
# clf = GradientBoostingClassifier()
# clf = GradientBoostingRegressor()
clf.fit(X, y)
# clf = sklearn.ensemble.RandomForestClassifier(500)
# clf.fit(X, y)

predict_day = 1217
reader_feature = csv.reader(file('output/features_%d.csv' % predict_day, 'rb'))
reader_result = csv.reader(file('output/y_%d.csv' % predict_day, 'rb'))

X = []
y = []
for (a, b) in zip(reader_feature, reader_result):
    X.append(map(lambda x: float(x), a[2:]))
    y.append(int(b[2]))


X = scalar.transform(X)
predict = clf.predict(X)


true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

real_buy = csv.reader(file('output/real_buy_%d.csv' % predict_day, 'r'))
buy_set = set()
for row in real_buy:
    buy_set.add(tuple(row))
reader_result = csv.reader(file('output/y_%d.csv' % predict_day, 'r'))
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
    X.append(map(lambda x: float(x), row[2:]))
  
X = scalar.transform(X)
predict = clf.predict(X)
  
writer = csv.writer(file('output/tianchi_mobile_recommendation_predict.csv', 'w'))
reader = csv.reader(file('output/features_1219.csv', 'r'))
    
writer.writerow(['user_id', 'item_id'])
for (x, y) in zip(reader, predict):
    if int(y) == 1:
        writer.writerow([str(x[0]), str(x[1])])
  
stop_time = time.clock()
print stop_time - start_time
