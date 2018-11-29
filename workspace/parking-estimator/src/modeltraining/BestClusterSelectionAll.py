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

    # n_cluster (positional)
    parser.add_argument('n_clusters', metavar='clusters', type=int, help='additionally provide the total number of clusters')
    # --all-datapoints (optional)
    parser.add_argument('--all-datapoints', action='store_true',
                        help='do not aggregate datapoints per timestamp, instead use all occupancy data')
    # --skip-training (optional)
    parser.add_argument('--skip-training', action='store_true',
                        help='skip the training phrase and load a model already available locally')
    # --test-all-datapoints (optional)
    parser.add_argument('--test-all-datapoints', action='store_true',
                        help='choose the clusters with all datapoints as testing bed')



    args = parser.parse_args()
    all_datapoints = args.all_datapoints
    skip_training = args.skip_training
    if skip_training is None:
        skip_training = False
    test_all_datapoints = args.test_all_datapoints
    n_clusters = args.n_clusters
    print("Executing with arguments: all-datapoints=" + str(all_datapoints)
            + " skip training: " + str(skip_training)
            + " test_all_datapoints: " + str(test_all_datapoints)
            + " n_clusters: " + str(n_clusters))

    print('Running Model Selection for ' + str(n_clusters) + ' clusters.')
    print
    for clusterId in range(n_clusters):
        print('--------------------')
        print( '     Cluster ' + str(clusterId) )
        print('--------------------')
	runSingle(clusterId, n_clusters, None, False, False, all_datapoints, skip_training, test_all_datapoints )
