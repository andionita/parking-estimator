'''
Created on 11.05.2017

@author: andigenu
Reduce the original occupancy datasheet (copy of SFpark_ParkingSensorData_HourlyOccupancy_20112013.csv)
to a smaller-size file that can be filtered and processed further
'''
import pandas as pd

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\original_occupancy.csv', sep=',')
#print(data.shape)
#print(data['STREET_BLOCK'], data['RATE'], data['START_TIME_DT'], data['TOTAL_TIME'], data['TOTAL_OCCUPIED_TIME'], data['TOTAL_VACANT_TIME'], data['TOTAL_UNKNOWN_TIME'], data['DAY_TYPE'])
intermediate = pd.concat([data['STREET_BLOCK'], data['START_TIME_DT'], data['DAY_TYPE'], data['TOTAL_TIME'], data['TOTAL_OCCUPIED_TIME'], data['TOTAL_VACANT_TIME'], data['TOTAL_UNKNOWN_TIME'], data['RATE']], axis=1)
intermediate.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_occupancy.csv', sep=',', index=False)
#print(intermediate)
