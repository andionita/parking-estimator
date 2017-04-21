'''
Created on 30.03.2017

@author: ionita
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.preprocessing import Imputer 

# read in data from csv file
#data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\all_blocks_for_prediction_minus_timestamp.csv', sep=',')
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\all_blocks_for_prediction_minus_timestamp_sample.csv', sep=',')

# fill in missing values with means of the REST of the data
imp = Imputer(missing_values='NaN', strategy='mean')
imp.fit(data)
array_imp = imp.transform(data)
data_imp = pd.DataFrame(array_imp, columns = data.columns)
#print(np.any(np.isnan(data)))
#print(np.all(np.isfinite(data)))

#data['OCCUPANCY'].hist()
#data.describe()
#data.dtypes

#plt.scatter(data['OCCUPANCY'], data['OCCUPANCY_1H'])
#plt.xlabel('OCCUPANCY')
#plt.ylabel('Counts')
#plt.show()

plt.scatter(data['OCCUPANCY'], data['OCCUPANCY_1H'])
plt.xlabel('OCCUPANCY')
plt.ylabel('Counts')
plt.show()

X = data_imp[list(data_imp.columns)[:-1]]
#print(X.shape)
y = data_imp['OCCUPANCY_1H']

#regressor = LinearRegression()
regressor = SGDRegressor(loss='squared_loss')
scores = cross_val_score(regressor, X, y, cv = 5)
print(scores.mean())
print(scores)

X_train, X_test, y_train, y_test = train_test_split(X, y)
regressor.fit(X_train, y_train)
xx = np.linspace(0, 26, 100)
yy = regressor.predict(xx.reshape(xx.shape[0], 1))
plt.plot(xx, yy)
#y_predictions = regressor.predict(X_test)
#print(regressor.score(X_test, y_test))
