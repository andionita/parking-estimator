'''
This module calls BestClusterModelSelection for every cluster with parking data in order to train
machine learning models

@author Andrei Ionita
'''
import argparse
import sqlalchemy
import pandas as pd
import sshtunnel
from sshtunnel import SSHTunnelForwarder
from BestClusterModelSelection import runSingle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Cluster Model Selection for all clusters')

    parser.add_argument('--all-datapoints', action='store_true',
                        help='do not aggregate datapoints per timestamp, instead use all occupancy data')

    args = parser.parse_args()
    all_datapoints = args.all_datapoints
    print("Executing with arguments: all-datapoints=" + str(all_datapoints))

    engine = sqlalchemy.create_engine('postgres://andio:andigenu@localhost:5432/sfpark')

    allClusters = pd.read_sql_query("""SELECT DISTINCT(cwithid) FROM blocks WHERE has_occupancy ORDER BY cwithid;""",
                                    engine)

    n_clusters = len(allClusters.index)
    print('Running Model Selection for ' + str(n_clusters) + ' clusters.')
    print
    for index, row in allClusters.iterrows():
        print('--------------------')
        print( '     Cluster ' + str(row['cwithid']) )
        print('--------------------')
        runSingle(row['cwithid'], n_clusters, None, False, False, all_datapoints )
