'''
Auxiliary Module to preprocess SFpark CSV files. Not part of the system workflow.

It takes the original SFpark parking occupancy data and processes it, so that it can be used as training data

@author Andrei Ionita
'''
import pandas as pd
import datetime
import math

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_occupancy.csv', sep=',')

data['OCCUPIED'] =  round(100 * data['TOTAL_OCCUPIED_TIME'] / (data['TOTAL_OCCUPIED_TIME'] + data['TOTAL_VACANT_TIME']), 3)
data['TOTAL_SPOTS'] = data['TOTAL_TIME'] // 3600
data['START_TIME_DT'] = pd.to_datetime(data['START_TIME_DT'], format='%d.%m.%Y %H:%M')
data['START_TIME_DT'] = data['START_TIME_DT'].dt.strftime('%Y-%m-%d %H:%M:%S')
data = data.drop(['TOTAL_TIME', 'TOTAL_OCCUPIED_TIME', 'TOTAL_VACANT_TIME', 'TOTAL_UNKNOWN_TIME'], axis=1)
data = data.rename(columns={'START_TIME_DT': 'TIMESTAMP', 'RATE': 'PRICE_RATE', 'PM_DISTRICT_NAME': 'DISTRICT', 'STREET_NAME': 'STREET'})
data.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy.csv', sep=',', index=False)
