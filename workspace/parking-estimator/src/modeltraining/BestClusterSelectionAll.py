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

    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))
    
    server.start()

    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')

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

    server.stop()
