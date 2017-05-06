'''
Created on 04.05.2017

@author: andigenu
'''
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, cross_val_score

# read from input file that has its missing values already filled
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_filled.csv', sep=',')

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']

#regressor = SVR(kernel='rbf', C=1e1, gamma=0.1)
#regressor = SVR(kernel='linear', C=1e3, cache_size=7000)
#regressor = SVR(kernel='poly', C=1e3, degree=2)
regressor = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5,
                   param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                               "gamma": np.logspace(-2, 2, 5)})

X_train, X_test, y_train, y_test = train_test_split(X, y)
print('Fitting the model...')
regressor.fit(X_train, y_train)
print('Predicting...')
print('R-squared: %.4f' % regressor.score(X_test, y_test))
scores = cross_val_score(regressor, X, y, cv = 10)
print(scores.mean())
print(scores)
