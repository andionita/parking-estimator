'''
Auxiliary Module to preprocess SFpark CSV files.

It takes the original SFpark traffic data and processes it, so that it can be potentially used as training data

@author Andrei Ionita
'''
import pandas as pd
import datetime as dt 
from datetime import timedelta
import math

records = []
for file_index in range(0,9):
    data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\original_traffic_' + str(file_index) + '.csv', sep=',')

    # per location aggregate information from quarter of hour to a full hour
    # average the traffic numbers towards the following hour (:15, :30, :45, :00)
    data = data.sort_values(by=['Location ID', 'Transmission Time'])
    
    traffic_occupancy = None
    vehicle_count = None
    median_speed = None
    average_speed = None
    group_count = 0
    last_locationid = None
    timestamp_nextentry = None 
    pos_index = 0
    for index, row in data.iterrows():
        pos_index += 1
        print(str(round(pos_index / data.shape[0], 2)) + ' file: ' + str(file_index) + '/4')

        # extract year from date (format: 2010-10-26 03:30:00)
        timestamp = dt.datetime.strptime(row['Transmission Time'], "%Y-%m-%d %H:%M:%S")
        if last_locationid is None:
            last_locationid = row['Location ID']
            if not math.isnan(row['Occupancy %']):
                traffic_occupancy = float(row['Occupancy %'])
            if not math.isnan(row['Vehicle Count']):
                vehicle_count = float(row['Vehicle Count'])
            if not math.isnan(row['Median Speed']):
                median_speed = float(row['Median Speed'])
            if not math.isnan(row['Average Speed']):
                average_speed = float(row['Average Speed'])
            group_count = 1
            # compute next time entry
            if timestamp.minute > 0:
                timestamp_nextentry = dt.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, 0, 0 ) + timedelta(hours=1)
            else:
                timestamp_nextentry = timestamp

        elif (last_locationid == row['Location ID'] and timestamp <= timestamp_nextentry):
            if not math.isnan(row['Occupancy %']):
                if traffic_occupancy is None:
                    traffic_occupancy = 0
                traffic_occupancy += float(row['Occupancy %'])
            if not math.isnan(row['Vehicle Count']):
                if vehicle_count is None:
                    vehicle_count = 0
                vehicle_count += float(row['Vehicle Count'])
            if not math.isnan(row['Median Speed']):
                if median_speed is None:
                    median_speed = 0
                median_speed += float(row['Median Speed'])
            if not math.isnan(row['Average Speed']):
                if average_speed is None:
                    average_speed = 0
                average_speed += float(row['Average Speed'])
            group_count += 1

        elif last_locationid != row['Location ID'] or timestamp > timestamp_nextentry:
            # add previous record
            if traffic_occupancy is not None:
                occupancy_avg = traffic_occupancy / group_count
            else:
                occupancy_avg = None
            if vehicle_count is not None:
                vehicle_count_avg = vehicle_count / group_count
            else:
                vehicle_count_avg = None
            if median_speed is not None:
                median_speed_avg = median_speed / group_count
            else:
                median_speed_avg = None
            if average_speed is not None:
                average_speed_avg = average_speed / group_count
            else:
                average_speed_avg = None
            record = {'LOCATION ID' : row['Location ID'], 'TIMESTAMP': timestamp_nextentry, 'STREET': row['Street Name'], 'DISTRICT': row['Parking Management District'],
                       'AVERAGE_TRAFFIC_OCCUPANCY': occupancy_avg, 'AVERAGE_VEHICLE_COUNT': vehicle_count_avg, 'MEDIAN_SPEED': median_speed_avg, 'AVERAGE_SPEED': average_speed_avg}
            records.append(record)

            # start collecting for the next record
            last_locationid = row['Location ID']
            traffic_occupancy = None
            vehicle_count = None
            median_speed = None
            average_speed = None
            if not math.isnan(row['Occupancy %']):
                traffic_occupancy = float(row['Occupancy %'])
            if not math.isnan(row['Vehicle Count']):
                vehicle_count = float(row['Vehicle Count'])
            if not math.isnan(row['Median Speed']):
                median_speed = float(row['Median Speed'])
            if not math.isnan(row['Average Speed']):
                average_speed = float(row['Average Speed'])
            group_count = 1
            # compute next time entry
            if timestamp.minute > 0:
                timestamp_nextentry = dt.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, 0, 0 ) + timedelta(hours=1)
            else:
                timestamp_nextentry = timestamp

    # added last record
    if traffic_occupancy is not None:
        occupancy_avg = traffic_occupancy / group_count
    if vehicle_count is not None:
        vehicle_count_avg = vehicle_count / group_count
    if median_speed is not None:
        median_speed_avg = median_speed / group_count
    if average_speed is not None:
        average_speed_avg = average_speed / group_count
    record = {'LOCATION ID' : row['Location ID'], 'TIMESTAMP': timestamp, 'STREET': row['Street Name'], 'DISTRICT': row['Parking Management District'],
               'AVERAGE_TRAFFIC_OCCUPANCY': occupancy_avg, 'AVERAGE_VEHICLE_COUNT': vehicle_count_avg, 'MEDIAN_SPEED': median_speed_avg, 'AVERAGE_SPEED': average_speed_avg}
    records.append(record)

result = pd.DataFrame(records)
result = result.reindex_axis(['LOCATION ID', 'TIMESTAMP', 'STREET', 'DISTRICT', 'AVERAGE_TRAFFIC_OCCUPANCY', 'AVERAGE_VEHICLE_COUNT', 'MEDIAN_SPEED', 'AVERAGE_SPEED'], axis=1)
result.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_traffic.csv', sep=',', index=False)         
