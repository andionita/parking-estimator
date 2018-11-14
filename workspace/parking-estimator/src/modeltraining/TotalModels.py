'''
This module trains models based on the entire parking data except one cluster with parking data.
The following methods are used for training: decision trees, svm, mlp, extreme gradient boosting
In total, |C| models will be trained and tested on respective the remaining cluster.
For the purpose of the thesis, it is enough that the results are written to stdout.

@author: Andrei Ionita
'''
import pandas as pd
import numpy as np
import xgboost as xg
import sqlalchemy
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import insert
from sqlalchemy import exc
import datetime
import time
import sys

import os.path
import sshtunnel
from sshtunnel import SSHTunnelForwarder

from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

from scipy.stats import uniform as sp_randreal


def queryAllExceptCluster( clusterId ):
    print("Querying database for all occupancy data, except for cluster id: " + str(clusterId))
    return pd.read_sql_query("""SELECT b.cwithid, o.timestamp, array_agg(o.block_id) AS blocks,
                                                    round(AVG(o.price_rate)::numeric,2) AS price_rate,
                                                    round(AVG(o.total_spots)::numeric,2) AS total_spots,
                                                    round(AVG(o.occupied)::numeric,2) AS occupied,
                                                    (SELECT array_agg(dimvalue) FROM cluster_cosine_vectors ccv WHERE b.cwithid = ccv.cid AND ccv.has_occupancy) as cosine,
                                                    (SELECT DISTINCT ON (cid, has_occupancy) emdvalue FROM cluster_emd_gaussians ceg WHERE ceg.cid = b.cwithid AND ceg.has_occupancy ) as emd
                                                    FROM occupancy o INNER JOIN blocks b ON o.block_id = b.block_id
                                                    WHERE b.has_occupancy AND b.cwithid <> """ + str(clusterId) + """
                                                    GROUP BY b.cwithid, o.timestamp
                                                    ORDER BY b.cwithid, o.timestamp;""", engine)


def queryCluster( clusterId ):
    print("Querying database for occupancy data for cluster id: " + str(clusterId))
    return pd.read_sql_query("""SELECT b.cwithid, o.timestamp, array_agg(o.block_id) AS blocks,
                                                    round(AVG(o.price_rate)::numeric,2) AS price_rate,
                                                    round(AVG(o.total_spots)::numeric,2) AS total_spots,
                                                    round(AVG(o.occupied)::numeric,2) AS occupied,
                                                    (SELECT array_agg(dimvalue) FROM cluster_cosine_vectors ccv WHERE b.cwithid = ccv.cid AND ccv.has_occupancy) as cosine,
                                                    (SELECT DISTINCT ON (cid, has_occupancy) emdvalue FROM cluster_emd_gaussians ceg WHERE ceg.cid = b.cwithid AND ceg.has_occupancy ) as emd
                                                    FROM occupancy o INNER JOIN blocks b ON o.block_id = b.block_id
                                                    WHERE b.has_occupancy AND cwithid = """ + str(clusterId) + """
                                                    GROUP BY b.cwithid, o.timestamp
                                                    ORDER BY b.cwithid, o.timestamp;""", engine)


def preprocess( trainingDataframe ):
    '''
    Removes unneeded columns from the dataframe containing training data
    :param trainingDataframe:
    :return: the resulting dataframe
    '''
    ts = trainingDataframe['timestamp']
    datetimes = pd.to_datetime(ts, format='%Y-%m-%d %H:%M:%S')
    dt = pd.DatetimeIndex(datetimes)
    trainingDataframe['year'] = dt.year
    trainingDataframe['week'] = dt.week
    trainingDataframe['weekday'] = dt.weekday
    trainingDataframe['hour'] = dt.hour
    trainingDataframe[['cosine_cat1', 'cosine_cat2', 'cosine_cat3']] = pd.DataFrame(trainingDataframe['cosine'].values.tolist(), index=trainingDataframe['cosine'].index)
    # drop unneeded columns
    trainingDataframe = trainingDataframe.drop(['timestamp'], axis=1)
    if 'blocks' in trainingDataframe.columns:
        trainingDataframe = trainingDataframe.drop(['blocks'], axis=1)
    trainingDataframe = trainingDataframe.drop(['cosine'], axis=1)
    return trainingDataframe


def buildModel( method, clusterId, X, y ):
    '''
    Trains a machine learning model using a given method (dt, svm, mlp or xgb) for a given cluster id and training data.
    :param method:
    :param clusterId:
    :param X: the input training data
    :param y: the output training data
    :return: the pair consisting of the resulting model object together with its training error
    '''
    filename = 'workspace/parking-estimator/persisted/total_extended_model_except_' + str(clusterId) + '_' + method + '.pkl'
    # In case we later want to skip model training and load a persisted model
    #if os.path.isfile(filename):
    #    print('Loading existing model...')
    #    model = joblib.load(filename)
    #    return (model, None)
    modelBest = None
    meanScore = None
    if method == 'dt':
        # DECISION TREES
        # Selecting the best dt model using Search Cross-Validation
        param_grid_dt = {"min_samples_split": [2, 3, 4, 5],
                         "min_samples_leaf": sp_randreal(0.03, 0.1),
                         # "min_samples_leaf": [0.04, 0.05, 0.06],
                         "max_features": [0.7, 0.8, 0.9, 1],
                         "criterion": ["mse", "mae"],
                         "min_weight_fraction_leaf": [0, 0.1, 0.2]
                         }
        model = DecisionTreeRegressor()
        modelBest = RandomizedSearchCV(model, param_distributions=param_grid_dt, n_iter=10)
    elif method == 'svm':
        # SUPPORT VECTOR MACHINES
        # In determining the best svm model, (Random) Search Cross-Validation was tried out
        param_grid_svr = {"C": [1e0, 1e1, 1e2, 1e3],
                          "gamma": np.logspace(-2, 2, 5)
                          # "C": sp_randreal(0.75, 1.25),
                          # "epsilon": sp_randreal(0.05, 0.5)
                          # "kernel": ["rbf", "sigmoid"],
                          # "degree": [2, 3, 4],
                          # "gamma": ["rbf", "poly", "sigmoid", "auto"],
                          # "coef0": [0, 0.5, 1, 10],
                          # "shrinking": [True, False]
                          }
        model = SVR(kernel="rbf", C=1.0, gamma=0.01);
        # modelBest = GridSearchCV(model, param_grid = param_grid_svr)
        # modelBest = RandomizedSearchCV(model, param_distributions=param_grid_svr, n_iter=5)
        modelBest = model
    elif method == 'mlp':
        # MULTILAYER PERCEPTRON
        # In determining the best mlp model, (Random) Search Cross-Validation was tried out
        param_grid_mlp_adam = {"activation": ["logistic", "tanh", "relu"],
                               # "solver": ["lbfgs", "sgd", "adam"]
                               # "learning_rate": ["constant", "invscaling", "adaptive"],
                               "shuffle": [True, False],
                               "early_stopping": [True, False],
                               "beta_1": sp_randreal(0, 1),
                               "beta_2": sp_randreal(0, 1)
                               }
        param_grid_mlp_sgd = {"activation": ["logistic", "tanh", "relu"],
                              # "solver": ["lbfgs", "sgd", "adam"]
                              "learning_rate": ["constant", "invscaling", "adaptive"],
                              "shuffle": [True, False],
                              # "power_t": sp_randreal(0, 1),
                              "momentum": sp_randreal(0, 1),
                              "nesterovs_momentum": [True, False],
                              "early_stopping": [True, False]
                              }
        model = MLPRegressor(hidden_layer_sizes=(7, 11), max_iter=500)
        #modelBest = GridSearchCV(model, param_grid = param_grid_mlp_adam)
        #modelBest = RandomizedSearchCV(model, param_distributions=param_grid_mlp_sgd, n_iter=10)
        modelBest = model
    elif method == 'xgb':
        # EXTREME GRADIENT BOOSTING
        # Selecting the best xgb model using Search Cross-Validation
        param_grid_xgb = {"max_depth": [2, 3],
                          "n_estimators": [50, 100],
                          "learning_rate": [0.1, 0.25],
                          # "booster": ["gbtree", "gblinear", "dart"],
                          # "gamma": [0, 0.1, 0.2],
                          # "min_child_weight": [1, 2, 3],
                          # "max_delta_step": [0, 1, 2],
                          # "subsample": [1, 2, 3]
                          # "colsample_bytree": [1],
                          # "colsample_bylevel": [1]
                          # etc.
                          }
        model = xg.XGBRegressor()
        modelBest = GridSearchCV(model, param_grid=param_grid_xgb)
        #modelBest = RandomizedSearchCV(model, param_distributions=param_grid_xgb, n_iter=10)
    print('Fitting the model with method ' + method + '...')
    modelBest.fit(X, y)
    # Performing cross-validation and determining the testing error using RMSE
    scores = cross_val_score(modelBest, X, y, cv=5, scoring='neg_mean_squared_error')
    meanScore = np.sqrt(-1 * scores.mean())
    print('Score was %.2f' % meanScore)
    print
    print(modelBest.get_params())
    print
    joblib.dump(modelBest, filename)
    print('Persisted model to file ' + filename)
    return (modelBest, meanScore)


def runSingleAll(clusterId, method):
    '''
    Runs the training and testing for a cluster and a given method.
    :param clusterId:
    :param method:
    :return:
    '''
    # Set the timestamp when this run is executed
    runTimestamp = datetime.datetime.now()
    runTimestamp.strftime('%Y-%m-%d %H:%M:%S')
    print
    print('-----> TRAINING MODELS <----')
    print
    # Retrieve training data (all minus given cluster)
    trainingDataframe = queryAllExceptCluster(clusterId)
    if len(trainingDataframe.index) == 0:
        print("Query for data returned empty set. Are you sure data exists except for the clusterid " + clusterId + "?")
    else:
        clusterDataframe = preprocess(trainingDataframe)
        print("\nNumber of samples = " + str(len(clusterDataframe.index)))
        X = clusterDataframe[['year', 'week', 'weekday', 'hour', 'price_rate', 'cosine_cat1', 'cosine_cat2', 'cosine_cat3', 'emd', 'total_spots']]
        y = clusterDataframe['occupied']
        models = {}
        trainingScores = {}
        timeElapsed = {}
        '''
        if method is not None:
            start = time.time()
            models[method], trainingScores[method] = buildModel(method, clusterId, X, y)
            timeElapsed[method] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed[method]))
        else:
            # build models for all methods (dt, svm, mlp, xgb)
            start = time.time()
            models['dt'], trainingScores['dt'] = buildModel('dt', clusterId, X, y)
            timeElapsed['dt'] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed['dt']))
            print('-----\n')
            start = time.time()
            models['svm'], trainingScores['svm'] = buildModel('svm', clusterId, X, y)
            timeElapsed['svm'] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed['svm']))
            print('-----\n')
            start = time.time()
            models['mlp'], trainingScores['mlp'] = buildModel('mlp', clusterId, X, y)
            timeElapsed['mlp'] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed['mlp']))
            print('-----\n')
            start = time.time()
            models['xgb'], trainingScores['xgb'] = buildModel('xgb', clusterId, X, y)
            timeElapsed['xgb'] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed['xgb']))
            print
        '''

        models['mlp'] = None
        trainingScores['mlp'] = 42.42
        timeElapsed['mlp'] = 422

        print
        print('----> SELECTING BEST MODELS <-----')
        print
        # Retrieve the cluster occupancy data for testing
        targetClusterData = queryCluster(clusterId)
        targetClusterData = preprocess(targetClusterData)
        X_test = targetClusterData[['year', 'week', 'weekday', 'hour', 'price_rate', 'cosine_cat1', 'cosine_cat2', 'cosine_cat3', 'emd', 'total_spots']]
        y_test = targetClusterData['occupied']
        # Determining the model with the best test error (RMSE)
        minError = 1001
        #selectedModel = None
        selectedModelName = None
        for modelName, modelContent in models.items():
            print('Testing model of type ' + modelName)
            if len(targetClusterData.index) == 0:
                print("Query for cluster " + str(clusterId) + " returned empty set. Please make sure that this cluster id exists.")
            else:
                '''
                y_pred = modelContent.predict(X_test)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                '''

                rmse = 42.44

                print('Model ' + str(modelName))
                print('RMSE = %.3f' % rmse)
                # Write model info into the database
                clusterid_stmt = (-1) * int(clusterId)
                model_name_stmt = str(modelName) + "_total_extended"
                stmt = modelsTable.insert().values(clusterid=1001,
                                                   data_points=len(clusterDataframe.index),
                                                   run_timestamp=runTimestamp, similar_clusterid=clusterId,
                                                   model_name=model_name_stmt, training_error=trainingScores[modelName],
                                                   error=rmse, error_type='RMSE',
                                                   training_time=timeElapsed[modelName])
                try:
                    conn.execute(stmt)
                #except exc.SQLAlchemyError as e:
                #except Exception as e:
                #    print(e)
                except sqlalchemy.exc.DataError as e:
                    print(e)
                except sqlalchemy.exc.ProgrammingError as e2:
                    print(e2)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                if rmse < minError:
                    minError = rmse
                    #selectedModel = modelContent
                    selectedModelName = modelName
            print
        print('Best model is ' + selectedModelName)
        print('----------------------------------\n')


if __name__ == "__main__":
    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))
    server.start()
    #engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:5432/sfpark')
    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')
    conn = engine.connect()
    modelsTable = Table('models', MetaData(engine), autoload=True)
    # Querying the cluster ids of the areas with parking data
    cwithidFrame = pd.read_sql_query("""SELECT DISTINCT ON (cwithid) cwithid FROM blocks WHERE has_occupancy""", engine);
    for index, row in cwithidFrame.iterrows():
        cwithid = row['cwithid']
        runSingleAll(cwithid, None)
    server.stop()
