'''
Created on 04.05.2017

@author: andigenu
'''
from sklearn.preprocessing import OneHotEncoder
import pandas as pd 

#enc = OneHotEncoder()
#enc.fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]])  
#print(enc.n_values_)
#print(enc.feature_indices_)

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_10p_prefilled.csv', sep=',')

enc = OneHotEncoder()

# need to provide a one column matrix to the encoder 
data_transformed = enc.fit_transform(data['BLOCK_ID'].as_matrix().reshape(-1, 1))
print(data_transformed.shape)
print(data_transformed.size)
print(data_transformed.dtype.itemsize)

# converting to a dense matrix so that it usable further
#data_transformed = data_transformed.todense()

# putting together columns into a new dataframe
result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
#result = pd.concat([pd.DataFrame(data_transformed, columns=['BLOCK_ID']), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
print(result.shape)
