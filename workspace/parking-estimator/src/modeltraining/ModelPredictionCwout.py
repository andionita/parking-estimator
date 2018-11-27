'''
This module computes the occupancy estimation of machine learning models for clusters without parking data

@author Andrei Ionita
'''
import argparse
import pandas as pd
import sqlalchemy
import json
import sshtunnel
from sshtunnel import SSHTunnelForwarder
from datetime import datetime, date, time, timedelta
from sklearn.externals import joblib

import BestClusterModelSelection as bcms


def get_cwout_results(simtype):
    '''
    Query all the clusters with parking data together with their similarity values towards clusters without parking data
    The clusters with parking data are ordered by similarity value.
    :param simtype: the similarity type (cosine, emd)
    :return: a dataframe containing the resulting associations of clusters without parking data
    and clusters with parking data
    '''
    order = "DESC"
    if simtype == "emd":
        order = "ASC"

    cwout_to_cwiths = pd.read_sql_query("""SELECT aux1.cid1 as cwoutid,
                                           array_agg(aux1.cid2 ORDER BY aux1.similarity """ + order + """) as cwithids,
                                           array_agg(aux1.similarity ORDER BY aux1.similarity """ + order + """)
                                           as similarities,
                                           array_agg(aux1.simtype ORDER BY aux1.similarity """ + order + """)
                                           as similarity_types,
                                           array_agg(aux2.model_name ORDER BY aux1.similarity """ + order + """)
                                           as model_names
                                    FROM
                                      (SELECT cid1,
                                              cid2,
                                              similarity,
                                              simtype
                                       FROM cluster_similarity
                                       WHERE NOT has1
                                         AND has2 AND simtype = '""" + simtype + """') AS aux1
                                    INNER JOIN
                                      (SELECT clusterid,
                                              model_name
                                       FROM models m
                                       WHERE run_timestamp =
                                           (SELECT MAX(run_timestamp)
                                            FROM models m2
                                            WHERE m2.clusterid = m.clusterid)
                                         AND error =
                                           (SELECT MIN(error)
                                            FROM models m3
                                            WHERE m3.run_timestamp = m.run_timestamp
                                              AND m3.clusterid = m.clusterid)) AS aux2
                                              ON aux1.cid2 = aux2.clusterid GROUP BY aux1.cid1;""", engine)
    return cwout_to_cwiths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute Estimations for Clusters without Data')
    # clusterId (positional argument)
    parser.add_argument('--simtype', help='similarity or distance, e.g. cosine or emd; by default cosine')

    parser.add_argument('--all-datapoints', action='store_true',
                            help='do not aggregate datapoints per timestamp, instead use all occupancy data')
    args = parser.parse_args()
    simtype = args.simtype
    all_datapoints = args.all_datapoints
    print("Executing with arguments simtype=" + str(simtype) + " and all_datapoints=" + str(all_datapoints))

    # Setting timestamps for training data to the following day, eight times thoughout the day
    today = datetime.today()
    timestamps = [  datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(0, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(3, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(6, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(9, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(12, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(15, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(18, 0)),
                    datetime.combine(date(today.year, today.month, today.day) + timedelta(days=1), time(21, 0))]
    testrecordsDict = {'timestamp': timestamps,
                    # price rate = average over total sfpark occupancy calculated beforehand
                    'price_rate': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    # total spots = average over total sfpark occupancy
                    'total_spots': [20, 20, 20, 20, 20, 20, 20, 20],
                    # blocks ids are not relevant
                    'blocks' : [ 0, 0, 0, 0, 0, 0, 0, 0]}

    testrecords = pd.DataFrame( testrecordsDict )

    testrecords = bcms.preprocess(testrecords)
    testrecords = testrecords[['year', 'week', 'weekday', 'hour', 'price_rate', 'total_spots']]

    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))
    server.start()
    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')

    # Query cwith - cwout associations for both cosine and emd similarities
    cwout_results_cosine = get_cwout_results('cosine')
    cwout_results_emd = get_cwout_results('emd')

    # Merge the dataframes
    cwout_results = pd.concat([cwout_results_cosine, cwout_results_emd]).sort_index(kind = 'merge')

    datapoints_str = 'agg'
    if all_datapoints:
        datapoints_str = 'all'
    resultingJsonArray = []
    # Iterate through the clusters without parking data and for each model with parking data compute an estimation
    # On odd iterations, estimations based on cosine similarity will be made
    # On even iterations, estimations based on emd will be made
    for index in range(0, len(cwout_results.index), 2):
        cwoutid = cwout_results.iloc[index]['cwoutid']
        cwithids = cwout_results.iloc[index]['cwithids']
        model_names = cwout_results.iloc[index]['model_names']
        similarities = cwout_results.iloc[index]['similarities']
        similarity_types = cwout_results.iloc[index]['similarity_types']

        innerJsonArray = []
        print('Processing Cluster Wout ' + str(cwoutid) )
        for i in range(0, len(cwithids)):
            filename = 'workspace/parking-estimator/persisted/clusterId' + str(cwithids[i]) + '_' + str(model_names[i]) + '_' + str(datapoints_str) + "_" + str(len(cwithids)) + '.pkl'
            model = joblib.load(filename)
            estimations = model.predict(testrecords)
            results = [{"timepoint" : str(t), "estimation": str(e)} for t, e in zip(timestamps, estimations)]

            innerJson = {}
            innerJson["cwithid"] = str(cwithids[i])
            innerJson["model_name"] = model_names[i]
            innerJson["similarity"] = str(similarities[i])
            innerJson["similarity_types"] = str(similarity_types[i])
            innerJson["results"] = results
            innerJsonArray.append(innerJson)

        cwoutid = cwout_results.iloc[index + 1 ]['cwoutid']
        cwithids = cwout_results.iloc[index + 1]['cwithids']
        model_names = cwout_results.iloc[index + 1]['model_names']
        similarities = cwout_results.iloc[index + 1]['similarities']
        similarity_types = cwout_results.iloc[index + 1]['similarity_types']

        for i in range(0, len(cwithids)):
            filename = 'workspace/parking-estimator/persisted/clusterId' + str(cwithids[i]) + '_' + str(model_names[i]) + '_' + str(datapoints_str) + "_" + str(len(cwithids)) + '.pkl'
            model = joblib.load(filename)
            estimations = model.predict(testrecords)
            results = [{"timepoint" : str(t), "estimation": str(e)} for t, e in zip(timestamps, estimations)]

            innerJson = {}
            innerJson["cwithid"] = str(cwithids[i])
            innerJson["model_name"] = model_names[i]
            innerJson["similarity"] = str(similarities[i])
            innerJson["similarity_types"] = str(similarity_types[i])
            innerJson["results"] = results
            innerJsonArray.append(innerJson)

        resultingJson = {}
        resultingJson["cwoutid"] = str(cwoutid)
        resultingJson["cwiths"] = innerJsonArray
        resultingJsonArray.append(resultingJson)

    # Save the timepoints as json
    with open('workspace/parking-estimator/jsons/estimations_cwout.json', 'w') as outfile:
        json.dump(resultingJsonArray, outfile)

    server.stop()
