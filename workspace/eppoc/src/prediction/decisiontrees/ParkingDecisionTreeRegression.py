'''
Created on 19.05.2017

@author: andigenu
'''
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.stats as stats
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR, LinearSVR, SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.feature_selection import SelectFromModel


# read in data from csv file
result = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy.csv', sep=',')
traffic = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\traffic_by_district.csv', sep=',')
#traffic = traffic.drop(['AVERAGE_TRAFFIC_OCCUPANCY'], axis=1)
traffic = traffic.drop(['AVERAGE_VEHICLE_COUNT'], axis=1)
traffic = traffic.drop(['MEDIAN_SPEED'], axis=1)
traffic = traffic.drop(['AVERAGE_SPEED'], axis=1)

print('Nr data records before merge: ' + str(len(result.index)))
result = pd.merge(result, traffic, on=['DISTRICT', 'TIMESTAMP'], how='left')
#print('Nr data records after merge: ' + str(len(result.index)))

timestamp = pd.to_datetime(result['TIMESTAMP'], format='%Y-%m-%d %H:%M:%S')
datetime = pd.DatetimeIndex(timestamp)
#result['YEAR'] = pd.DatetimeIndex(result['TIMESTAMP']).year
result['YEAR'] = datetime.year
#result['CALENDAR_WEEK'] = pd.to_datetime(result['TIMESTAMP'], format='%d.%m.%Y %H:%M')
result['CALENDAR_WEEK'] = datetime.week
#result['WEEKDAY'] = pd.DatetimeIndex(result['TIMESTAMP']).weekday
result['WEEKDAY'] = datetime.weekday
#result['HOUR'] = pd.DatetimeIndex(result['TIMESTAMP']).hour
result['HOUR'] = datetime.hour
#print(result)

result['PRICE_RATE'] = result['PRICE_RATE'].fillna(0)
#result = result[pd.notnull(result['AVERAGE_TRAFFIC_OCCUPANCY'])]
result['AVERAGE_TRAFFIC_OCCUPANCY'] = result['AVERAGE_TRAFFIC_OCCUPANCY'].fillna(0)
#result['AVERAGE_VEHICLE_COUNT'] = result['AVERAGE_VEHICLE_COUNT'].fillna(0)
#result['MEDIAN_SPEED'] = result['MEDIAN_SPEED'].fillna(0)
#result['AVERAGE_SPEED'] = result['AVERAGE_SPEED'].fillna(0)
result = result[pd.notnull(result['OCCUPIED'])]

result = result.drop(['TIMESTAMP'], axis=1)
result = result.drop(['DAY_TYPE'], axis=1)
result = result.drop(['STREET'], axis=1)

#print(result)

encoder_block = LabelEncoder()
blocks_transformed = encoder_block.fit(result['STREET_BLOCK'].as_matrix())
encoder_distrct = LabelEncoder()
district_transformed = encoder_distrct.fit(result['DISTRICT'].as_matrix())
#encoder_street = LabelEncoder()
#street_transformed = encoder_street.fit(result['STREET'].as_matrix())
'''
#encoder_weekday = LabelEncoder()
label_encoder_weekday = LabelEncoder()
encoder_weekday = OneHotEncoder()
# need to provide a one column matrix to the encoder
#weekday_transformed = encoder_weekday.fit_transform(data['DAY_TYPE'].as_matrix())
label_weekday_transformed = label_encoder_weekday.fit_transform(data['DAY_TYPE'].as_matrix())
weekday_transformed = encoder_weekday.fit_transform(label_weekday_transformed.reshape(-1, 1))
# converting to a dense matrix so that it usable further
# putting together columns into a new dataframe
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['MONTH'], data['DAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.reshape(-1, 1), columns=['DAY_TYPE']), data['OCCUPIED']], axis=1)
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.reshape(-1, 1), columns=['DAY_TYPE']), data['OCCUPIED']], axis=1)
#result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['MONTH'], data['DAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.todense()), data['OCCUPIED']], axis=1)
result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['YEAR'], data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], data['OCCUPIED']], axis=1)
#result = pd.concat([pd.DataFrame(blocks_transformed.reshape(-1, 1), columns=['STREET_BLOCK']), data['YEAR'], data['CALENDAR_WEEK'], data['WEEKDAY'], data['HOUR'], data['TOTAL_SPOTS'], data['PRICE_RATE'], pd.DataFrame(weekday_transformed.todense(), columns=['IS_WEEKDAY', 'IS_WEEKEND']), data['OCCUPIED']], axis=1)
'''

'''
def isWeekday(day):
    if day == 'weekday':
        return 0
    else:
        return 1

result['DAY_TYPE'] = result['DAY_TYPE'].apply(isWeekday)
'''
#result['STREET_BLOCK'] = result['STREET_BLOCK'].astype('category')
result['STREET_BLOCK'] = encoder_block.transform(result['STREET_BLOCK'].as_matrix())
#result[['OCCUPIED']] = result[['OCCUPIED']].astype(int)
result['DISTRICT'] = district_transformed.transform(result['DISTRICT'].as_matrix())
#result['STREET'] = street_transformed.transform(result['STREET'].as_matrix())

result = result.sort_values(by=['STREET_BLOCK', 'YEAR', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR'])

X = result[['STREET_BLOCK', 'YEAR', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR', 'TOTAL_SPOTS', 'DISTRICT', 'AVERAGE_TRAFFIC_OCCUPANCY']]
y = result['OCCUPIED']

#X_train, X_test, y_train, y_test = train_test_split(X, y)
dataset_threshold_p = 0.9
dataset_threshold = int(len(X.index) * dataset_threshold_p)
X_train = X[:dataset_threshold]
X_test = X[dataset_threshold + 1:]
y_train = y[:dataset_threshold]
y_test = y[dataset_threshold + 1:]
'''
# Filter features

# Saving dataframe (original index, streetblock, date)
pre_regressor = ExtraTreesRegressor()

print('Fitting the model for feature selection...')
pre_regressor.fit(X_train, y_train)
print(X_train.columns.values)
print(pre_regressor.feature_importances_)

print('Rating the importance of individual features...')
selector = SelectFromModel(pre_regressor, prefit=True, threshold=0.05)
#selector = SelectFromModel(pre_regressor, prefit=True)
Xnew_train = selector.transform(X_train)
Xnew_test = selector.transform(X_test)
print('Original no of features: ' + str(len(X_train.columns)))
print('New no of features: ' + str(Xnew_train.shape[1]))

print('Filtered-in columns: ' + str(X_train.columns[selector.get_support()].values))
filteredout_columns = X_train.columns[np.invert(selector.get_support())].values
X_train = X_train.drop(filteredout_columns, axis=1)
X_test = X_test.drop(filteredout_columns, axis=1)
'''
regressor = DecisionTreeRegressor()

print('Fitting the model...')
regressor.fit(X_train, y_train)

print('Predicting...')
print('R-squared: %.4f' % regressor.score(X_test, y_test))
#scores = cross_val_score(regressor, X, y, cv = 5)
#print(scores.mean())

y_predicted = regressor.predict(X_test)
test = pd.concat([X_test, y_test], axis=1)
#print('test length: ' + str(len(test.index)) )

test['PREDICTED'] = y_predicted.reshape(-1,1)

# average the occupancy values per hour
avg_hours = test.groupby(['HOUR'])['OCCUPIED'].mean()

# generate scatter-plots (with interpolation) for single days with real occupancy (green) vs predicted occupancy (red)
# works as expected only when split of train + test data is clean (not randomous)
listfigs = []
xCurrent = []
ytestCurrent = []
ypredCurrent = []
yavgCurrent = []
indexFig = 0
better_than, better_than_total, better_than_avg = 0, 0, 0
trend, trend_total = 0, 0
deviations = []
for i, r in test.iterrows():
    figid = 'Block: ' + str(int(result.loc[i, 'STREET_BLOCK'])) + ', Year: ' + str(int(result.loc[i, 'YEAR'])) + ', Week: ' + str(int(result.loc[i, 'CALENDAR_WEEK'])) + ', Weekday: ' + str(int(result.loc[i, 'WEEKDAY']))
    if listfigs.count(figid) == 0:
        #print('len(xCurrent) = ' + str(len(xCurrent)))
        if len(listfigs) > 0 and len(xCurrent) >= 20:
            # plot previous figure
            indexFig += 1
            #if int(result.loc[i, 'STREET_BLOCK']) == 369 and int(result.loc[i, 'YEAR']) == 2013 and int(result.loc[i, 'CALENDAR_WEEK']) == 1 and (int(result.loc[i, 'WEEKDAY']) == 2 or int(result.loc[i, 'WEEKDAY']) == 3):
            #print(figid)
            #print('xCurrent len: ' + str(len(xCurrent)))
            #print(xCurrent)
            #print('ytestCurrent len: ' + str(len(ytestCurrent)))
            #print(ytestCurrent)
            #print('ypredCurrent len: ' + str(len(ypredCurrent)))
            #print(ypredCurrent)
            
            for ihour in range(len(xCurrent)):
                better_than_total += 1
                if abs(ytestCurrent[ihour] - ypredCurrent[ihour]) <= 5.0:
                    better_than += 1                
                if abs(ytestCurrent[ihour] - ypredCurrent[ihour]) < abs(avg_hours[int(ihour)] - ytestCurrent[ihour]):
                    better_than_avg += 1
                deviations.append(abs(ytestCurrent[ihour] - ypredCurrent[ihour]))

            for ihour in range(1, len(xCurrent)):
                if ((ytestCurrent[ihour] == ytestCurrent[ihour - 1]) and (ypredCurrent[ihour] == ypredCurrent[ihour - 1])) or ((ytestCurrent[ihour] - ytestCurrent[ihour - 1]) * (ypredCurrent[ihour] - ypredCurrent[ihour - 1]) > 0):
                    trend += 1
                trend_total += 1
            '''
            xLin = np.linspace(min(xCurrent), max(xCurrent), num=500, endpoint=True)
            #df1 = pd.DataFrame({'x': xCurrent, 'y': ytestCurrent})
            #df1 = df1.sort_values(by=['y'])
            #df2 = pd.DataFrame({'x': xCurrent, 'y': ypredCurrent})
            #df2 = df2.sort_values(by=['y'])
            #f1 = interp1d(df1['x'], df1['y'])
            f1 = interp1d(xCurrent, ytestCurrent)
            #f2 = interp1d(df2['x'], df2['y'])
            f2 = interp1d(xCurrent, ypredCurrent)
            f3 = interp1d(xCurrent, yavgCurrent)            

            diff_ar = []
            for j in range(len(ytestCurrent)):
                diff_ar.append(abs(ytestCurrent[j] - ypredCurrent[j]))
            std_err = stats.sem(diff_ar)
            diff_ar.sort()
            weights = np.ones_like(diff_ar)/(float(len(diff_ar)))
            distrib = stats.norm.pdf(diff_ar, np.mean(diff_ar), np.std(diff_ar))
            distrib_plot = plt.figure(2*indexFig)
            distrib_plot.suptitle(listfigs[len(listfigs) - 1] + ' - Std Error: ' + str(round(std_err, 2)) + '%')
            #plt.plot(diff_ar, distrib_perc)
            plt.plot(diff_ar, distrib)
            plt.hist(diff_ar, weights = weights)
            plt.xlabel('Deviation (%)')
            plt.ylabel('Events (%)') 
            #plt.axis([0, 50, 0, 10])           
            
            fig = plt.figure(2*indexFig+1)
            fig.suptitle(listfigs[len(listfigs) - 1])
            plt.plot(xCurrent, ytestCurrent, 'o', color='green')
            plt.plot(xLin, f1(xLin), '-', color='green')
            plt.plot(xCurrent, ypredCurrent, 'o', color='red')
            plt.plot(xLin, f2(xLin), '-', color='red')
            plt.plot(xCurrent, yavgCurrent, 'o', color='orange')
            plt.plot(xLin, f3(xLin), '--', color='orange')
            plt.xlabel('Hours')
            plt.ylabel('Occupancy')
            plt.legend(['data real', '', 'data predicted', ''])
            #plt.legend(['data real', '', 'data predicted', '', 'data average', ''])
            plt.axis([0, 23, 0, 100])
            if indexFig == 10:
                break
            '''
        listfigs.append(figid)
        # reset for new figure
        xCurrent = []
        ytestCurrent = []
        ypredCurrent = []
        yavgCurrent = []        
    if xCurrent.count(int(r['HOUR'])) == 0:
        xCurrent.append(int(r['HOUR']))
        ytestCurrent.append(r['OCCUPIED'])
        ypredCurrent.append(r['PREDICTED'])
        yavgCurrent.append(avg_hours[int(r['HOUR'])])
        '''
        if abs(r['OCCUPIED'] - r['PREDICTED']) <= 5.0:
            better_than += 1
        better_than_total += 1
        if abs(r['OCCUPIED'] - r['PREDICTED']) < abs(avg_hours[int(r['HOUR'])] -  r['OCCUPIED']):
            better_than_avg += 1
        deviations.append(abs(r['OCCUPIED'] - r['PREDICTED']))
        '''
    
plt.show()
print('Better or equal to 95%: ' + str(round(better_than / better_than_total, 3)))
print('Better than average %: ' + str(round(better_than_avg / better_than_total, 3)))
print('Trend %: ' + str(round(trend / trend_total, 3)))
print('Standard Error: ' + str(round(stats.sem(deviations), 3)))
