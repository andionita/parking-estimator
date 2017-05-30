'''
Created on 02.05.2017

@author: andigenu
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.kernel_approximation import RBFSampler
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

# read in data from csv file
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

X = result[list(result.columns)[:-1]]
y = result['OCCUPIED']

#X_train, X_test, y_train, y_test = train_test_split(X, y)
dataset_threshold_p = 0.9
dataset_threshold = int(len(X.index) * dataset_threshold_p)
X_train = X[:dataset_threshold]
X_test = X[dataset_threshold + 1:]
y_train = y[:dataset_threshold]
y_test = y[dataset_threshold + 1:]

rbf_feature = RBFSampler(gamma=1, random_state=1)
X_features = rbf_feature.fit_transform(X)
# other loss methods are: 'squared_loss', 'huber', 'epsilon_insensitive', or 'squared_epsilon_insensitive'
regressor = SGDRegressor(loss='huber')

regressor.fit(X_train, y_train)
print('R-squared: %.4f' % regressor.score(X_test, y_test))
#scores = cross_val_score(regressor, X, y, cv = 5)
#print(scores.mean())
#print(scores)

y_predicted = regressor.predict(X_test)
test = pd.concat([X_test, y_test], axis=1)
test['PREDICTED'] = y_predicted.reshape(-1,1)

test = test.sort_values(by=['STREET_BLOCK', 'CALENDAR_WEEK', 'WEEKDAY', 'HOUR'])

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
