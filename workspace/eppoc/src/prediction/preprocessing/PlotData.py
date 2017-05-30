'''
Created on 18.05.2017

@author: andigenu
'''
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# read from input file that has its missing values already filled 
#data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_daymonth.csv', sep=',')
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',')
print('Reading data completed.')

encoder_block = LabelEncoder()
#encoder_weekday = LabelEncoder()
label_encoder_weekday = LabelEncoder()
encoder_weekday = OneHotEncoder()
# need to provide a one column matrix to the encoder 
blocks_transformed = encoder_block.fit_transform(data['STREET_BLOCK'].as_matrix())
#weekday_transformed = encoder_weekday.fit_transform(data['DAY_TYPE'].as_matrix())
label_weekday_transformed = label_encoder_weekday.fit_transform(data['DAY_TYPE'].as_matrix())
weekday_transformed = encoder_weekday.fit_transform(label_weekday_transformed.reshape(-1, 1))
# converting to a dense matrix so that it usable further
# putting together columns into a new dataframe
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['MONTH'], data['DAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.reshape(-1, 1), columns=['DAY_TYPE']), data['OCCUPIED']], axis=1)
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.reshape(-1, 1), columns=['DAY_TYPE']), data['OCCUPIED']], axis=1)
#result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['MONTH'], data['DAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.todense()), data['OCCUPIED']], axis=1)
result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.todense(), columns=['IS_WEEKDAY', 'IS_WEEKEND']), data['OCCUPIED']], axis=1)
print('Encoding data completed.')

result = result.sort_values(by=['STREET_BLOCK', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR'])

# block 10, 15, 16
# generate aggregated scatter-plots for first StreetBlocks and weekday/weekend
# precondition: dataframe needs to be sorted by street block
special_block = 16
found = False
for i, r in result.iterrows():
    streetBlock = int(r['STREET_BLOCK'])
    if streetBlock != special_block:
        if found:
            break    
        continue
    found = True
    fig = plt.figure(1)
    fig.suptitle('Block ' + str(special_block) + ' - Weekday')
    fig = plt.figure(2)
    fig.suptitle('Block ' + str(special_block) + ' - Weekend')
    if int(r['IS_WEEKDAY']) == 1: 
        plt.figure(1)
        plt.scatter(r['HOUR'], r['OCCUPIED'], s=1)
    else:
        plt.figure(2)
        plt.scatter(r['HOUR'], r['OCCUPIED'], s=1)
plt.show()

'''
# generate aggregated scatter-plots for first StreetBlocks and days of the week
for i, r in X.iterrows():
    streetBlock = r['STREET_BLOCK']
    fig = plt.figure(1)
    fig.suptitle('Monday')
    fig = plt.figure(2)
    fig.suptitle('Tuesday')
    fig = plt.figure(3)
    fig.suptitle('Wednesday')
    fig = plt.figure(4)
    fig.suptitle('Thursday')
    fig = plt.figure(5)
    fig.suptitle('Friday')
    fig = plt.figure(6)
    fig.suptitle('Saturday')
    fig = plt.figure(7)
    fig.suptitle('Sunday')
    for index, row in X.iterrows():
        if row['STREET_BLOCK'] == streetBlock:
            plt.figure(int(row['WEEKDAY']))
            plt.scatter(row['HOUR'], y[index], s=1)
        else:
            break
    break    
plt.show()
'''

'''
# generate aggregated scatter-plots for separate StreetBlocks
# precondition: dataframe needs to be sorted by street block
lastStreetBlock = None
noBlocks = 0
for i, r in result.iterrows():
    streetBlock = r['STREET_BLOCK']
    if lastStreetBlock != streetBlock:
        if noBlocks == 20:
            break
        # start new figure
        lastStreetBlock = streetBlock
        noBlocks += 1
        fig = plt.figure(noBlocks)
        fig.suptitle('Block ' + str(int(streetBlock)))
        plt.xlabel('Hours')
        plt.ylabel('Occupancy Rate')
    plt.scatter(r['HOUR'], r['OCCUPIED'], s=1)
plt.show()    
'''

'''
lastStreetBlock = None
noBlocks = 0
for i, r in result.iterrows():
    streetBlock = r['STREET_BLOCK']
    if lastStreetBlock == streetBlock:
        continue
    lastStreetBlock = streetBlock
    noBlocks += 1
    if noBlocks == 10:
        break
    fig = plt.figure(noBlocks)
    fig.suptitle('Block ' + str(int(streetBlock)))
    found = False
    for index, row in result.iterrows():
        if row['STREET_BLOCK'] == streetBlock:
            plt.scatter(row['HOUR'], r['OCCUPIED'], s=1)
            found = True
        elif found:
            break
    plt.xlabel('Hours')
    plt.ylabel('Occupancy Rate')
plt.show()
'''