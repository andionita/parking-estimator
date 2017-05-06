'''
Created on 02.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.feature_extraction import DictVectorizer 

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_sample.csv', sep=',')
#data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp.csv', sep=',')
data['BLOCK_ID'] = data['BLOCK_ID'].astype(str)
print(data.dtypes)

# fill in missing values with means of the REST of the data
imp = Imputer(missing_values='NaN', strategy='mean')
imp.fit(data)
array_imp = imp.transform(data)
data_imp = pd.DataFrame(array_imp, columns = data.columns)
data_imp.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\all_blocks_for_prediction_minus_timestamp_sample_filled.csv', sep=',', index=False)

v = DictVectorizer(sparse=False)
v.fit(data['BLOCK_ID'])
print(v.transform(data['BLOCK_ID']))
