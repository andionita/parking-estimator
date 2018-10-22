'''
Auxiliary Module to preprocess SFpark CSV files. Not part of the system workflow.

It reduce the original occupancy datasheet (copy of SFpark_ParkingSensorData_HourlyOccupancy_20112013.csv)
to a smaller-size file, so that can be filtered and processed further.

@author Andrei Ionita
'''
import pandas as pd

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\original_occupancy.csv', sep=',')

intermediate = pd.concat([data['STREET_BLOCK'], data['START_TIME_DT'], data['DAY_TYPE'], data['TOTAL_TIME'], data['TOTAL_OCCUPIED_TIME'], data['TOTAL_VACANT_TIME'], data['TOTAL_UNKNOWN_TIME'], data['RATE'], data['PM_DISTRICT_NAME'], data['STREET_NAME']], axis=1)
intermediate.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_occupancy.csv', sep=',', index=False)
