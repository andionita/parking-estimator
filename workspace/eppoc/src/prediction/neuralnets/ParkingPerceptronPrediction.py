'''
Created on 02.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import PolynomialFeatures


# read from input file that has its missing values already filled 
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_filled.csv', sep=',')

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']
print(y.shape)

# convert floats into ints so they can be classified
X = PolynomialFeatures(interaction_only=True).fit_transform(X).astype(int)
y = y.values.reshape((-1, 1))
y = PolynomialFeatures(interaction_only=True).fit_transform(y).astype(int)
y = y.reshape((-1,))

classifier = Perceptron(n_iter=10, eta0=1)
X_train, X_test, y_train, y_test = train_test_split(X, y)
classifier.fit(X_train, y_train )
predictions = classifier.predict(X_test)

print('R-squared: %.4f' % classifier.score(X_test, y_test))
scores = cross_val_score(classifier, X, y, cv = 10)
print(classifier.mean())
print(classifier)
