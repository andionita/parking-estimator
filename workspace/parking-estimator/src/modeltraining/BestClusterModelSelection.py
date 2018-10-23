'''
This module builds models for clusters with parking data. Four methods will be used: decision trees, svm, mlp,
extreme gradient boosting. The resulting models are afterwards tested on all the other clusters.
Finally, the models are persisted and information about them is stored in the database, such as
cluster on which it was trained, train error, cluster on which it was tested, test error, etc.

Input parameters:
- cluster id
- method
- nodb -> option of not writing the results in the database
- noeval -> option of not evaluating the built models

Usage:
BestClusterModelSelection.py [-h] [--method METHOD] [--nodb] [--noeval] clusterId

@author Andrei Ionita
'''
import argparse

import sqlalchemy
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select, insert
import sshtunnel
from sshtunnel import SSHTunnelForwarder

import pandas as pd
import os.path
import numpy as np
import datetime
import time
import sys

import xgboost as xg

from sklearn.externals import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, cross_val_score
from sklearn.svm import SVR
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, explained_variance_score

from scipy.stats import uniform as sp_randreal

def queryClusterAll( clusterId, engine ):
    '''
    Retrieve occupancy data from a cluster with parking data
    :param clusterId:
    :param engine:
    :return: the dataframe resulting from the database result query
    '''
    print("Querying database for occupancy data for cluster id: " + str(clusterId))

    return pd.read_sql_query("""SELECT b.cwithid, o.timestamp, o.block_id AS blocks,
                                                    o.price_rate AS price_rate,
                                                    o.total_spots AS total_spots,
                                                    o.occupied AS occupied
                                                    FROM occupancy o INNER JOIN blocks b ON o.block_id = b.block_id
                                                    WHERE b.has_occupancy AND cwithid = """ + str(clusterId) + """
                                                    ORDER BY b.cwithid, o.timestamp;""", engine)

def queryClusterAvg( clusterId, engine ):
    '''
    Retrieve occupancy data from a cluster with parking data by averaging the features among the blocks
    :param clusterId:
    :param engine:
    :return: the dataframe resulting from the database result query
    '''
    print("Querying database for occupancy data for cluster id: " + str(clusterId))

    return pd.read_sql_query("""SELECT b.cwithid, o.timestamp, array_agg(o.block_id) AS blocks,
                                                    round(AVG(o.price_rate)::numeric,2) AS price_rate,
                                                    round(AVG(o.total_spots)::numeric,2) AS total_spots,
                                                    round(AVG(o.occupied)::numeric,2) AS occupied
                                                    FROM occupancy o INNER JOIN blocks b ON o.block_id = b.block_id
                                                    WHERE b.has_occupancy AND cwithid = """ + str(clusterId) + """
                                                    GROUP BY b.cwithid, o.timestamp
                                                    ORDER BY b.cwithid, o.timestamp;""", engine)


def preprocess( clusterDataframe ):
    '''
    Removes unneeded columns from the dataframe containing training data
    :param clusterDataframe:
    :return: the resulting dataframe
    '''
    ts = clusterDataframe['timestamp']
    datetimes = pd.to_datetime(ts, format='%Y-%m-%d %H:%M:%S')

    dt = pd.DatetimeIndex(datetimes)

    clusterDataframe['year'] = dt.year
    clusterDataframe['week'] = dt.week
    clusterDataframe['weekday'] = dt.weekday
    clusterDataframe['hour'] = dt.hour

    clusterDataframe = clusterDataframe.drop(['timestamp'], axis=1)
    clusterDataframe = clusterDataframe.drop(['blocks'], axis=1)

    return clusterDataframe


def buildModel( method, clusterId, X, y ):
    '''
    Trains a machine learning model using a given method (dt, svm, mlp or xgb) for a given cluster id and training data.
    :param method:
    :param clusterId:
    :param X: the input training data
    :param y: the output training data
    :return: the pair consisting of the resulting model object together with its training error
    '''
    filename = 'workspace/parking-estimator/persisted/clusterId' + str(clusterId) + '_' + method + '.pkl'

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

        model = xg.XGBRegressor();
        modelBest = GridSearchCV(model, param_grid = param_grid_xgb)
        #modelBest = RandomizedSearchCV(model, param_distributions=param_grid_xgb, n_iter=10)
        #modelBest = model

    print('Fitting the model for cluster id ' + str(clusterId) + ' with method ' + method + '...')
    modelBest.fit(X, y)

    # Performing cross-validation and determining the testing error using RMSE
    scores = cross_val_score(modelBest, X, y, cv=5, scoring='neg_mean_squared_error')
    meanScore = np.sqrt(-1 * scores.mean())
    print('Score was %.2f' % meanScore)
    print

    print(modelBest.get_params())
    print

    joblib.dump(modelBest, filename)
    print('Persisted model to file ' + filename )

    return (modelBest, meanScore)


def runSingle(clusterId, method, nodb, noeval):
    '''
    Runs the training and testing for a cluster and a given method.
    :param clusterId:
    :param method:
    :param nodb:
    :param noeval:
    :return:
    '''

    # Set the timestamp when this run is executed
    runTimestamp = datetime.datetime.now()
    runTimestamp.strftime('%Y-%m-%d %H:%M:%S')

    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))

    server.start()

    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')
    conn = engine.connect()

    print
    print('-----> TRAINING MODELS <----')
    print
    # Retrieve training data for cluster
    clusterDataframe = queryClusterAvg(clusterId, engine)
    #clusterDataframe = queryClusterAll(clusterId, engine)

    if len(clusterDataframe.index) == 0:
        print("Query for cluster " + str(clusterId) + " returned empty set. Are you sure this clusterId exists?")

    else:

        clusterDataframe = preprocess(clusterDataframe)
        print("\nNumber of samples = " + str(len(clusterDataframe.index)))

        X = clusterDataframe[['year', 'week', 'weekday', 'hour', 'price_rate', 'total_spots']]
        y = clusterDataframe['occupied']

        models = {}
        trainingScores = {}
        timeElapsed = {}

        if method is not None:
            start = time.time()
            models[method], trainingScores[method] = buildModel(method, clusterId, X, y)
            timeElapsed[method] = time.time() - start
            print('Time elapsed: ' + str(timeElapsed[method]))

        else:
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

        if noeval:
            sys.exit()

        print
        print('----> SELECTING BEST MODELS <-----')
        print

        # Retrieve the most similar clusters (with data) according to the similarity measure
        similarClusters = pd.read_sql_query("""SELECT DISTINCT ON (cid2) cid2 FROM cluster_similarity cs
                                            WHERE cid1 = """ + str(clusterId) + """ AND has1 AND has2""", engine)

        metadata = MetaData(engine)

        modelsTable = Table('models', metadata, autoload=True)

        for index, row in similarClusters.iterrows():
            simClusterId = int(row['cid2'])

            similarClusterData = queryClusterAvg(simClusterId, engine)
            #similarClusterData = queryClusterAll(simClusterId, engine)
            similarClusterData = preprocess(similarClusterData)

            X_test = similarClusterData[['year', 'week', 'weekday', 'hour', 'price_rate', 'total_spots']]
            y_test = similarClusterData['occupied']

            # Determining the model with the best test error (RMSE)
            minError = 101
            selectedModel = None
            selectedModelName = None
            for modelName, modelContent in models.items():
                print('Determining best model for cwith id ' + str(simClusterId) +
                      ' with model from cluster ' + str(clusterId) +
                      ' of type ' + modelName)

                if len(similarClusterData.index) == 0:
                    print("Query for cluster " + str(simClusterId) + " returned empty set. "
                                                                     "Please make sure that this cluster id exists.")

                else:
                    y_pred = modelContent.predict(X_test)

                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    print('RMSE = %.3f' % rmse)

                    if not nodb:
                        # Write model info into the database
                        stmt = modelsTable.insert().values(clusterid = clusterId,
                                                           data_points = len(clusterDataframe.index),
                                                    run_timestamp = runTimestamp, similar_clusterid = simClusterId,
                                                    model_name = modelName, training_error = trainingScores[modelName],
                                                    error = rmse, error_type = 'RMSE',
                                                    training_time = timeElapsed[modelName])
                        conn.execute(stmt)

                    if rmse < minError:
                        minError = rmse
                        selectedModel = modelContent
                        selectedModelName = modelName
                print

            print('Best model is ' + selectedModelName)
            print('----------------------------------\n')

    server.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select the best Estimating Model for a Cluster by building or '
                                                 'load it, if it already exists')
    # clusterId (positional argument)
    parser.add_argument('clusterId', metavar='clusterId', type=int, help='cluster id (cwithid)')
    # --method (optional)
    parser.add_argument('--method',
                        help='enforcing building a model using the specified method; '
                             'if left out, the best model will be built/loaded')
    # --nodb (optional)
    parser.add_argument('--nodb', action='store_true',
                        help='do not write the results into the database')
    # --noeval (optional)
    parser.add_argument('--noeval', action='store_true',
                        help='skip the phase of selecting best model for similar clusters')
    args = parser.parse_args()

    clusterId = args.clusterId
    method = args.method
    if method is not None:
        method = method.lower()
    nodb = args.nodb
    noeval = args.noeval
    print("Executing with arguments " + str(clusterId) + " method: " + str(method)
            + " nodb: " + str(nodb) + " noeval: " + str(noeval))
    print

    # Train models for a cluster and method
    runSingle(clusterId, method, nodb, noeval)
