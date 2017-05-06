'''
Created on 06.05.2017

@author: andigenu
'''
import pandas as pd

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_all_filled.csv', sep=',')
data = data.sort_values(['CALENDAR_WEEK', 'DAY_OF_WEEK', 'HOUR'])
#print(data.shape)
data5p = data.head(52428)

data5p.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_5p_prefilled.csv', sep=',', index=False)
