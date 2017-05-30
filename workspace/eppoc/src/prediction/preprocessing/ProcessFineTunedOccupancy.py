'''
Created on 11.05.2017

@author: andigenu
'''
import pandas as pd
import datetime
import math

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_occupancy.csv', sep=',')

data['OCCUPIED'] =  round(100 * data['TOTAL_OCCUPIED_TIME'] / (data['TOTAL_OCCUPIED_TIME'] + data['TOTAL_VACANT_TIME']), 3)
data['TOTAL_SPOTS'] = data['TOTAL_TIME'] // 3600
#data['TIMESTAMP'] = datetime.datetime.strptime(data['START_TIME_DT'], "%d.%m.%Y %H:%M")
data['START_TIME_DT'] = pd.to_datetime(data['START_TIME_DT'], format='%d.%m.%Y %H:%M')
data['START_TIME_DT'] = data['START_TIME_DT'].dt.strftime('%Y-%m-%d %H:%M:%S')
print(data)
data = data.drop(['TOTAL_TIME', 'TOTAL_OCCUPIED_TIME', 'TOTAL_VACANT_TIME', 'TOTAL_UNKNOWN_TIME'], axis=1)
data = data.rename(columns={'START_TIME_DT': 'TIMESTAMP', 'RATE': 'PRICE_RATE', 'PM_DISTRICT_NAME': 'DISTRICT', 'STREET_NAME': 'STREET'})
#print(data)
data.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy.csv', sep=',', index=False)

'''
d = []
for index, row in data.iterrows():
    print(index)
    # unknown_time then skip record (no data on occupancy can be drawn)
    if row['TOTAL_TIME'] == row['TOTAL_UNKNOWN_TIME']:
        print('Skipping row: TOTAL_TIME is equal to TOTAL_UNKNOWN_TIME')
        continue
    # extract year from date (format: 01.04.2011 00:00)
    date = datetime.datetime.strptime(row['START_TIME_DT'], "%d.%m.%Y %H:%M")
    year = date.year
    # extract month or calendar week
    month = date.month
    calendarweek = date.isocalendar()[1]
    # extract day or day of week   
    day = date.day    
    weekday = date.weekday() + 1
    # extract hour
    hour = date.hour
    # calculate no. of spots
    if row['TOTAL_TIME'] % 3600 != 0:
        print('WARN: TOTAL_TIME is not divisible by 3600 as it should')
    noSpots =  row['TOTAL_TIME'] // 3600
    rate = row['RATE']
    if math.isnan(rate):
        rate = 0.0
    # calculate occupancy
    occupancy = round(row['TOTAL_OCCUPIED_TIME'] / ( row['TOTAL_OCCUPIED_TIME'] + row['TOTAL_VACANT_TIME']) * 100, 3)
    #record = {'STREET_BLOCK': row['STREET_BLOCK'], 'YEAR': year, 'MONTH': month, 'DAY': day, 'DAY_TYPE': row['DAY_TYPE'], 'HOUR': hour, 'TOTAL_SPOTS': noSpots, 'OCCUPIED': occupancy, 'PRICE_RATE': rate, 'DISTRICT': row['PM_DISTRICT_NAME'], 'STREET': row['STREET_NAME'] }
    record = {'STREET_BLOCK': row['STREET_BLOCK'], 'YEAR': year, 'CALENDAR_WEEK': calendarweek, 'WEEKDAY': weekday, 'DAY_TYPE': row['DAY_TYPE'], 'HOUR': hour, 'TOTAL_SPOTS': noSpots, 'OCCUPIED': occupancy, 'PRICE_RATE': rate, 'DISTRICT': row['PM_DISTRICT_NAME'], 'STREET': row['STREET_NAME'] }
    d.append(record)    
result = pd.DataFrame(d)

# reorder columns to soothe our preferences
#result = result.reindex_axis(['STREET_BLOCK', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'DAY_TYPE', 'TOTAL_SPOTS', 'PRICE_RATE', 'DISTRICT', 'STREET', 'OCCUPIED'], axis=1)
result = result.reindex_axis(['STREET_BLOCK', 'YEAR', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR', 'DAY_TYPE', 'TOTAL_SPOTS', 'PRICE_RATE', 'DISTRICT', 'STREET', 'OCCUPIED'], axis=1)
#result.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_daymonth.csv', sep=',', index=False)
result.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',', index=False)
'''
