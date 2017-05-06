'''
Created on 02.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.linear_model import Lasso, LassoLars
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# read from input file that has its missing values already filled 
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_10p_prefilled.csv', sep=',')

#encoder = LabelEncoder()
encoder = OneHotEncoder()
# need to provide a one column matrix to the encoder 
#data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix())
data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix().reshape(-1, 1))
# putting together columns into a new dataframe
#result = pd.concat([pd.DataFrame(data_transformed.reshape(-1, 1), columns=['BLOCK_ID']), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']

regressor = Lasso(alpha = 0.1)
#regressor = LassoLars(alpha=.1)

X_train, X_test, y_train, y_test = train_test_split(X, y)
regressor.fit(X_train, y_train)
print('R-squared: %.4f' % regressor.score(X_test, y_test))
scores = cross_val_score(regressor, X, y, cv = 10)
print(scores.mean())
print(scores)
