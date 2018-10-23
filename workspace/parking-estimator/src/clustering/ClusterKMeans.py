'''
This module computes applies K-Means++ clustering on the city blocks

Input parameters: n_clusters - the number of clusters with parking data

@author Andrei Ionita
'''
from shapely import wkt
from sqlalchemy import MetaData, Table, update
from sklearn.cluster import KMeans
from sshtunnel import SSHTunnelForwarder

import pandas as pd
import numpy as np
import sqlalchemy
import sshtunnel

import math
import argparse

def cluster_zone(has_occupancy, no_clusters_zone, blockTable, engine):
    '''
    Clusters a zone (with parking data, without parking data) into a given number of clusters and writes the results
    in the database.
    :param has_occupancy:
    :param no_clusters_zone:
    :param blockTable:
    :param engine:
    :return:
    '''
    query_condition = ""
    if not has_occupancy:
        query_condition = "NOT"

    # Retrieves all blocks belonging to a particular city zone
    query = """SELECT
                    ST_AsText(b.wkt) as geom,
                    b.block_id,
                    aux.no_amenities
                FROM blocks b
                LEFT JOIN
                    (SELECT mbp.block_id,
                        count(*) AS no_amenities
                    FROM merge_block_poi mbp
                    GROUP BY mbp.block_id) AS aux ON b.block_id = aux.block_id
                WHERE """ + query_condition + " has_occupancy;"""

    blocks = pd.read_sql(query, engine)

    # Preparing the kmeans++ input as point arrays, by assigning the blocks coordinates
    n_geom = len(blocks.index)
    points = np.zeros((n_geom, 2))
    blocksMap = {}
    for index, row in blocks.iterrows():
        geom = wkt.loads(row['geom'])
        centroid = geom.centroid
        x, y = centroid.coords.xy
        points[index][0] = x[0]
        points[index][1] = y[0]
        blocksMap[index] = row['block_id']

    kmeans = KMeans(n_clusters = no_clusters_zone).fit(points)

    # Write cluster ids in the database, table blocks
    for i in range(n_geom):
        if has_occupancy:
            stmt = blocksTable.update().where(blocksTable.c.block_id == blocksMap[i]).values(cwithid = int(kmeans.labels_[i]))
        else:
            stmt = blocksTable.update().where(blocksTable.c.block_id == blocksMap[i]).values(cwoutid = int(kmeans.labels_[i]))
        conn.execute(stmt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cluster blocks into a predefined number of areas')
    parser.add_argument('n_clusters', metavar='clusters', type=int, help='number of clusters')
    args = parser.parse_args()

    # The number of predefined clusters
    cwith_no = args.n_clusters

    cwout_no = int(2.6 * cwith_no)
    total = cwith_no + cwout_no
    print("Clustering SFpark blocks into a total of " +  str(total) + " areas")
    print
    print( str(cwith_no) + " areas have parking data, " + str(cwout_no) + " have no parking data")
    print

    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))

    server.start()

    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')
    conn = engine.connect()
    metadata = MetaData(engine)
    blocksTable = Table('blocks', metadata, autoload=True)

    cluster_zone(True, cwith_no, blocksTable, engine)
    cluster_zone(False, int(cwith_no * 2.6), blocksTable, engine)

    server.stop()

    print("Clustering finished.")
