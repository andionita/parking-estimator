'''
Created on 30.03.2017

@author: ionita
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import Imputer, LabelEncoder, OneHotEncoder 

# read in data from csv file
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_5p_prefilled.csv', sep=',')

#encoder = LabelEncoder()
encoder = OneHotEncoder()
#data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix())
data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix().reshape(-1, 1))

#data = pd.concat([pd.DataFrame(data_transformed.reshape(-1, 1), columns=['BLOCK_ID']), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
data = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']
X_train, X_test, y_train, y_test = train_test_split(X, y)

quadratic_featurizer = PolynomialFeatures(degree=2)
X_train_quad = quadratic_featurizer.fit_transform(X_train)
X_test_quad = quadratic_featurizer.fit_transform(X_test)

regressor_quad = LinearRegression()
regressor_quad.fit(X_train_quad, y_train)
print('R-squared: %.4f' % regressor_quad.score(X_test_quad, y_test))
scores = cross_val_score(regressor_quad, X, y, cv = 10)
print(scores.mean())
print(scores)


