'''
Created on 29.04.2017

@author: andigenu
'''

from sklearn.neural_network import MLPClassifier

# EXAMPLE 1
'''X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X, y)
print(clf.predict([[2., 2.], [-1., -2.]]))
print([coef.shape for coef in clf.coefs_])'''

# EXAMPLE 2
'''X = [[0., 0.], [1., 1.]]
y = [[0, 1], [1, 1]]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
print(clf.fit(X, y))
print(clf.predict([[1., 2.]]))
print(clf.predict([[0., 0.]]))'''

# EXAMPLE 3
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
#print(cancer.keys())
#print(cancer.data.shape)
#print(cancer.target.shape)
#print(cancer.target_names)
#print(cancer.DESCR)
#print(cancer.feature_names)
X = cancer['data']
y = cancer['target']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
print(scaler.fit(X_train))
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# three hidden layers with as many neurons as features in the data set
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
print(mlp.fit(X_train,y_train))
predictions = mlp.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))