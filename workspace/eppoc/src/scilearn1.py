from sklearn import datasets
iris = datasets.load_iris()
digits = datasets.load_digits()
#print(digits.images[0])

from sklearn import svm
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[ :-1])
#print(clf.predict(digits.data[-1:]))

#persist model to string
import pickle
s = pickle.dumps(clf)
clf2 = pickle.loads(s)
print(clf2.predict(digits.data[2:3]))
print(digits.target[2])

#persist model to file
from sklearn.externals import joblib
joblib.dump(clf, '../persisted/scilearn1.pkl')
clf = joblib.load('../persisted/scilearn1.pkl')
print(clf2.predict(digits.data[0:1]))
print(digits.target[0])

boston = datasets.load_boston()
#print(boston.target)