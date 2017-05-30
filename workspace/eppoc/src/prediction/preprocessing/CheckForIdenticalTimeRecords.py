'''
Created on 20.05.2017

@author: andigenu
'''
import pandas as pd
import numpy as np

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',')
print(data)

data = data.sort_values(by=['STREET_BLOCK', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR'])
print(data)

last_record = None
last_record_full = None
last_record_index = None
no = 0
for index, row in data.iterrows():
    if last_record is not None:
        if (row.values[:4] == last_record).all():
            print(str(last_record_index))
            print(last_record_full)
            print(str(index))
            print(row.values)            
            no += 1
    last_record = row.values[:4]
    last_record_full = row.values
    last_record_index = index
print(no)