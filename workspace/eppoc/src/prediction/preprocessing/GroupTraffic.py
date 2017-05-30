'''
Created on 26.05.2017

@author: andigenu
'''
import pandas as pd

data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\essential_traffic.csv', sep=',')

avg_traffic_occ = data.groupby(['DISTRICT', 'TIMESTAMP'])['AVERAGE_TRAFFIC_OCCUPANCY'].mean()
avg_traffic_occ_df = pd.DataFrame({'AVERAGE_TRAFFIC_OCCUPANCY' : avg_traffic_occ}).reset_index()
#print(avg_traffic_occ_df)
avg_vehicle_count = data.groupby(['DISTRICT', 'TIMESTAMP'])['AVERAGE_VEHICLE_COUNT'].mean()
avg_vehicle_count_df = pd.DataFrame({'AVERAGE_VEHICLE_COUNT' : avg_vehicle_count}).reset_index()
#print(avg_vehicle_count_df)
median_speed = data.groupby(['DISTRICT', 'TIMESTAMP'])['MEDIAN_SPEED'].mean()
median_speed_df = pd.DataFrame({'MEDIAN_SPEED' : median_speed}).reset_index()
#print(median_speed_df)
avg_speed = data.groupby(['DISTRICT', 'TIMESTAMP'])['AVERAGE_SPEED'].mean()
avg_speed_df = pd.DataFrame({'AVERAGE_SPEED' : avg_speed}).reset_index()
#print(avg_speed_df)

results = pd.merge(pd.merge(pd.merge(avg_traffic_occ_df, avg_vehicle_count_df, on=['DISTRICT', 'TIMESTAMP']), median_speed_df, on=['DISTRICT', 'TIMESTAMP']), avg_speed_df, on=['DISTRICT', 'TIMESTAMP'])
#print(results)
results.to_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\traffic_by_district.csv', sep=',', index=False)
