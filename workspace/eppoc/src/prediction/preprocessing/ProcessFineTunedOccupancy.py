'''
Created on 11.05.2017

@author: andigenu
'''
import pandas as pd
import datetime
import math

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_occupancy.csv', sep=',')

d = []
for index, row in data.iterrows():
    print(index)
    # unknown_time then skip record (no data on occupancy can be drawn)
    if row['TOTAL_TIME'] == row['TOTAL_UNKNOWN_TIME']:
        print('Skipping row: TOTAL_TIME is equal to TOTAL_UNKNOWN_TIME')
        continue
    # extract year from date (format: 01.04.2011 00:00)
    date = datetime.datetime.strptime(row['START_TIME_DT'], "%d.%m.%Y %H:%S")
    #year = date.year
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
    #record = {'STREET_BLOCK': row['STREET_BLOCK'], 'MONTH': month, 'DAY': day, 'DAY_TYPE': row['DAY_TYPE'], 'HOUR': hour, 'TOTAL_SPOTS': noSpots, 'OCCUPIED': occupancy, 'PRICE_RATE': rate}
    record = {'STREET_BLOCK': row['STREET_BLOCK'], 'CALENDAR_WEEK': calendarweek, 'WEEKDAY': weekday, 'DAY_TYPE': row['DAY_TYPE'], 'HOUR': hour, 'TOTAL_SPOTS': noSpots, 'OCCUPIED': occupancy, 'PRICE_RATE': rate}
    d.append(record)    

result = pd.DataFrame(d)
# reorder columns to soothe our preferences
#result = [['STREET_BLOCK', 'MONTH', 'DAY', 'HOUR', 'DAY_TYPE', 'TOTAL_SPOTS', 'OCCUPIED', 'PRICE_RATE']]
result = result.reindex_axis(['STREET_BLOCK', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR', 'DAY_TYPE', 'TOTAL_SPOTS', 'OCCUPIED', 'PRICE_RATE'], axis=1)
#result.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_daymonth.csv', sep=',', index=False)
result.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',', index=False)
