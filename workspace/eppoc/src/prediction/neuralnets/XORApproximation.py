'''
Created on 30.04.2017

@author: andigenu
Source: From Mastering Machine Learning with scikit-learn p.212
'''
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

y = [0, 1, 1, 0] * 1000
#print(len(y))
X = [[0, 0], [0, 1], [1, 0], [1, 1]] * 1000
#print(len(X))
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
print('Size of training (X_train = %s, y_train = %s) samples' % (len(X_train), len(y_train)))
print('Size of training (X_test = %s, y_test = %s) samples' % (len(X_test), len(y_test)))
clf = MLPClassifier(hidden_layer_sizes=(2,), activation='logistic', solver='sgd', random_state=3)
clf.fit(X_train, y_train)
print('Number of layers: %s. Number of outputs: %s' % (clf.n_layers_, clf.n_outputs_))
predictions = clf.predict(X_test)
print('Accuracy:', clf.score(X_test, y_test))
for i, p in enumerate(predictions[:10]):
    print('True: %s, Predicted: %s' % (y_test[i], p))
