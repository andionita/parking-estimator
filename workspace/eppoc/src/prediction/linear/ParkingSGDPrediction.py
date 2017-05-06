'''
Created on 02.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.kernel_approximation import RBFSampler

# read from input file that has its missing values already filled 
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_filled.csv', sep=',')

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']

rbf_feature = RBFSampler(gamma=1, random_state=1)
X_features = rbf_feature.fit_transform(X)
regressor = SGDRegressor(loss='huber')
# other loss methods are: 'squared_loss', 'huber', 'epsilon_insensitive', or 'squared_epsilon_insensitive'

X_train, X_test, y_train, y_test = train_test_split(X, y)
regressor.fit(X_train, y_train)
print('R-squared: %.4f' % regressor.score(X_test, y_test))
scores = cross_val_score(regressor, X, y, cv = 5)
print(scores.mean())
print(scores)
