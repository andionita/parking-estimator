'''
This module calls BestClusterModelSelection for every cluster with parking data in order to train
machine learning models

@author Andrei Ionita
'''
import argparse
import sqlalchemy
import pandas as pd

from BestClusterModelSelection import runSingle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Cluster Model Selection for all clusters')

    engine = sqlalchemy.create_engine('postgres://andio:andigenu@localhost:5432/sfpark')

    allClusters = pd.read_sql_query("""SELECT DISTINCT(cwithid) FROM blocks WHERE has_occupancy ORDER BY cwithid;""",
                                    engine)

    total = len(allClusters.index)
    print('Running Model Selection for ' + str(total) + ' clusters.')
    print
    for index, row in allClusters.iterrows():
        print('--------------------')
        print( '     Cluster ' + str(row['cwithid']) )
        print('--------------------')
        runSingle(row['cwithid'], None, False, False )

