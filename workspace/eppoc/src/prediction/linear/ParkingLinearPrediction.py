'''
Created on 30.03.2017

@author: ionita
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d 
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# read from input file that has its missing values already filled 
#data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_daymonth.csv', sep=',')
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data_sklearn\\tuned_occupancy_calendarweek.csv', sep=',')

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

'''
result['OCCUPANCY'].hist()
data.describe()
data.dtypes
'''

X = result[list(result.columns)[:-1]]
y = result['OCCUPIED']

regressor = LinearRegression()
#regressor = SGDRegressor(loss='squared_loss')

dataset_threshold_p = 0.9
dataset_threshold = int(len(X.index) * dataset_threshold_p)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
X_train = X[:dataset_threshold]
X_test = X[dataset_threshold + 1:]
y_train = y[:dataset_threshold]
y_test = y[dataset_threshold + 1:]

regressor.fit(X_train, y_train)
y_predicted = regressor.predict(X_test)
test = pd.concat([X_test, y_test], axis=1)

test['PREDICTED'] = y_predicted.reshape(-1,1)

print('R-squared: %.4f' % regressor.score(X_test, y_test))
#scores = cross_val_score(regressor, X, y, cv = 10)
#print(scores.mean())
#print(scores)

'''
# generate scatter-plots for composed single days (made up of different day information) with real occupancy (green) vs predicted occupancy (red)
noFigures = 1
iteration = 0
xLast = []
ytestLast = []
ypredLast = []
index = 0
for i, r in X_test.iterrows():
    index += 1
    if xLast.count(int(r['HOUR'])) == 0:
        iteration += 1
        xLast.append(int(r['HOUR']))
        ytestLast.append(y_test.iloc[index])
        ypredLast.append(y_predicted[index])
    if iteration == 24:
        f1 = interp1d(xLast, ytestLast)
        f2 = interp1d(xLast, ypredLast)
        xLin = np.linspace(0, 23, num=1000, endpoint=True)
        fig = plt.figure()
        fig.suptitle('Day ' + str(noFigures))
        plt.plot(xLast, ytestLast, 'o', color='green')
        plt.plot(xLin, f1(xLin), '-', color='green')
        plt.plot(xLast, ypredLast, 'o', color='red')
        plt.plot(xLin, f2(xLin), '-', color='red')
        plt.legend(['data real', '', 'data predicted', ''])
        xLast = []
        ytestLast = []
        ypredLast = []
        if noFigures == 10:
            break;
        noFigures += 1
        iteration = 0
plt.show()
'''        

test = test.sort_values(by=['STREET_BLOCK', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR'])
#print(test.to_string(columns = ['STREET_BLOCK', 'WEEKDAY', 'HOUR', 'OCCUPIED', 'PREDICTED']))

# generate scatter-plots (with interpolation) for single days with real occupancy (green) vs predicted occupancy (red)
# works as expected only when split of train + test data is clean (not randomous)
listfigs = []
xCurrent = []
ytestCurrent = []
ypredCurrent = []
indexFig = 0
for i, r in test.iterrows():
    figid = 'Block: ' + str(int(r['STREET_BLOCK'])) + ', Week: ' + str(int(r['CALENDAR_WEEK'])) + ', Weekday: ' + str(int(r['WEEKDAY']))
    if listfigs.count(figid) == 0:
        listfigs.append(figid)        
        if indexFig > 0:
            # plot previous figure
            xLin = np.linspace(min(xCurrent), max(xCurrent), num=100, endpoint=True)
            df1 = pd.DataFrame({'x': xCurrent, 'y': ytestCurrent})
            df1 = df1.sort_values(by=['y'])
            df2 = pd.DataFrame({'x': xCurrent, 'y': ypredCurrent})
            df2 = df2.sort_values(by=['y'])
            f1 = interp1d(df1['x'], df1['y'])
            f2 = interp1d(df2['x'], df2['y'])
            plt.plot(xCurrent, ytestCurrent, 'o', color='green')
            plt.plot(xLin, f1(xLin), '-', color='green')
            plt.plot(xCurrent, ypredCurrent, 'o', color='red')
            plt.plot(xLin, f2(xLin), '-', color='red')
            plt.legend(['data real', '', 'data predicted', ''])
        if indexFig == 10:
            break        
        # reset for new figure
        indexFig += 1 
        xCurrent = []
        ytestCurrent = []        
        ypredCurrent = []        
        fig = plt.figure(indexFig)
        fig.suptitle(figid)
    if xCurrent.count(int(r['HOUR'])) == 0:
        xCurrent.append(int(r['HOUR']))
        ytestCurrent.append(r['OCCUPIED'])
        ypredCurrent.append(r['PREDICTED'])
plt.show()

'''
# generate scatter-plots for single days with real occupancy (green) vs predicted occupancy (red)
blocks = []
hours = []
index = 0
newblocks = 0
storeReal = {}
storePred = {}
for i, r in X_test.iterrows():
    index += 1
    print(index)
    figtitle = str(int(r['STREET_BLOCK'])) + '_' + str(int(r['CALENDAR_WEEK'])) + '_' + str(r['WEEKDAY'])
    figdetail = str(int(r['STREET_BLOCK'])) + '_' + str(int(r['CALENDAR_WEEK'])) + '_' + str(r['WEEKDAY']) + '_' + str(r['HOUR'])
    figid = int(r['STREET_BLOCK'])
    if hours.count(figdetail) > 0:
        # happens that the same day in two different years appears 
        continue
    if blocks.count(figtitle) == 0:
        #if newblocks == 10:
        #    continue
        newblocks += 1            
    if blocks.count(figtitle) < 24:
        if blocks.count(figtitle) == 0:
            storeReal[figtitle] = []
            storePred[figtitle] = []
        storeReal[figtitle].insert(int(r['HOUR']), y_test.iloc[index])        
        storePred[figtitle].insert(int(r['HOUR']), y_predicted[index])
        hours.append(figdetail)
        blocks.append(figtitle)
    else:
        # happens that the same day in two different years appears
        continue

for key, value in storeReal.items():
    print( key + ': ' + str(len(value)))
'''

'''    
fig = plt.figure(figid)        
fig.suptitle(figtitle)
plt.scatter(r['HOUR'], y_test.iloc[index], s=1, color='green')
plt.scatter(r['HOUR'], y_predicted[index], s=1, color='red')
plt.show()
'''


'''regressor = SGDRegressor(loss='squared_loss')
scores = cross_val_score(regressor, X, y, cv = 5)
print(scores.mean())
print(scores)'''

'''X_train, X_test, y_train, y_test = train_test_split(X, y)
regressor.fit(X_train, y_train)
xx = np.linspace(0, 26, 100)
yy = regressor.predict(xx.reshape(xx.shape[0], 1))
plt.plot(xx, yy)'''
#y_predictions = regressor.predict(X_test)
#print(regressor.score(X_test, y_test))
