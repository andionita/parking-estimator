'''
Created on 04.05.2017

@author: andigenu
'''
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd
import numpy as np 

label_encoder = LabelEncoder()
onehot_encoder = OneHotEncoder()
'''
#data_transformed = enc.fit_transform([[0], [1], [0], [2]])  
data_labeled = label_encoder.fit_transform(['weekday', 'weekend', 'weekend', 'weekday'])
data_transformed = onehot_encoder.fit_transform(data_labeled.reshape(-1, 1))
print(data_transformed.todense())
'''

#data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_10p_prefilled.csv', sep=',')
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',')
print(data.dtypes)

print(data['DAY_TYPE'].as_matrix())
data_labeled = label_encoder.fit_transform(data['DAY_TYPE'].as_matrix())
print(data_labeled)
#data_transformed = enc.fit_transform(data['BLOCK_ID'].as_matrix().reshape(-1, 1))
data_transformed = onehot_encoder.fit_transform(data_labeled.reshape(-1, 1))
print(data_transformed.todense())
print(data_transformed.shape)
print(data_transformed.size)
print(data_transformed.dtype.itemsize)

# converting to a dense matrix so that it usable further
#data_transformed = data_transformed.todense()

# putting together columns into a new dataframe
#result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
#result = pd.concat([data['STREET_BLOCK'], data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(data_transformed.todense()), data['OCCUPIED']], axis=1)
#print(result.shape)
