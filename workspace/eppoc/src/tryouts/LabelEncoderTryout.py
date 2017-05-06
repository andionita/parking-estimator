'''
Created on 04.05.2017

@author: andigenu
'''
from sklearn.preprocessing import LabelEncoder
import pandas as pd

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_filled.csv', sep=',')
#print(data.dtypes)
#print(data['BLOCK_ID'].as_matrix())

enc = LabelEncoder()
data_transformed = enc.fit_transform(data['BLOCK_ID'].as_matrix())
#print(data_transformed)

result = pd.concat([pd.DataFrame(data_transformed.reshape(-1, 1), columns=['BLOCK_ID']), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
print(result.dtypes)
print(result.shape)

'''le = LabelEncoder()
le.fit([1, 2, 2, 6])
print(le.classes_)
print(le.transform([1, 1, 2, 6])) 
print(le.inverse_transform([0, 0, 1, 2]))'''
