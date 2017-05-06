'''
Created on 04.05.2017

@author: andigenu
'''
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.kernel_approximation import RBFSampler
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.pipeline import make_pipeline

# read from input file that has its missing values already filled 
data = pd.read_csv('C:\\Users\\andigenu\\parking\\sfpark\\training_data\\sklearn\\bare_blocks_10p_prefilled.csv', sep=',')

#encoder = LabelEncoder()
encoder = OneHotEncoder()
# need to provide a one column matrix to the encoder 
#data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix())
data_transformed = encoder.fit_transform(data['BLOCK_ID'].as_matrix().reshape(-1, 1))
# converting to a dense matrix so that it usable further
# putting together columns into a new dataframe
#result = pd.concat([pd.DataFrame(data_transformed.reshape(-1, 1), columns=['BLOCK_ID']), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)
result = pd.concat([pd.DataFrame(data_transformed.todense()), data['CALENDAR_WEEK'], data['DAY_OF_WEEK'], data['HOUR'], data['OCCUPANCY'], data['OCCUPANCY_1H']], axis=1)

X = data[list(data.columns)[:-1]]
y = data['OCCUPANCY_1H']

regressor = MLPRegressor(hidden_layer_sizes=(8,12));
X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()  
scaler.fit(X_train)  
X_train = scaler.transform(X_train)  
X_test = scaler.transform(X_test)  

regressor.fit(X_train, y_train) 
print('R-squared: %.4f' % regressor.score(X_test, y_test))

pipeline = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(8,12)))
scores = cross_val_score(pipeline, X, y, cv = 5)
print(scores.mean())        
print(scores)
