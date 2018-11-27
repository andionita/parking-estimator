'''
This module computes the EMD Gaussians for every cluster. Afterwards, it computes the Earth Mover's Distance between
all Gaussians.

A EMD Gaussian are computed based on public amenity information. More precisely, a EMD Gaussian is equal to the
linear combination of Gaussian that have mean = stay duration and standard deviation = stay duration stddev.

@author Andrei Ionita
'''
from pyemd import emd
import sqlalchemy
from sqlalchemy import MetaData, Table
import numpy as np
import ot
import pandas as pd
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance
import sshtunnel
from sshtunnel import SSHTunnelForwarder

def calculateGaussianForCwith(cid):
    '''
    Computes the EMD Gaussian for a given cluster with parking data
    :param cid:
    :return: the resulting EMD Gaussian, as array
    '''
    amenitiesForClustersWith = pd.read_sql_query("""SELECT c.cid,
                                                               a.name,
                                                               c.dimvalue,
                                                               a.mean_duration,
                                                               a.stdev_duration
                                                        FROM cluster_emd_gaussians c
                                                        INNER JOIN amenities a ON c.dimname = a.name
                                                        WHERE c.has_occupancy AND c.cid = """ + str(cid) + """
                                                        ORDER BY a.name""", engine)
    current_sum = 0
    current_gaussian = np.zeros((n_bins))
    for index, row in amenitiesForClustersWith.iterrows():
        if row['stdev_duration'] == 0 or np.isnan(row['stdev_duration']):
            continue
        current_sum += row['dimvalue']
        #current_gaussian += row['dimvalue'] * ot.datasets.get_1D_gauss(n_bins,
#                                                                       m=offset + row['mean_duration'],
#                                                                       s=row['stdev_duration'])
        current_gaussian += row['dimvalue'] * ot.datasets.make_1D_gauss(n_bins,
                                                                    m = offset + row['mean_duration'],
                                                                    #m = row['mean_duration'],
                                                                    s = row['stdev_duration'])
    magnitude = 0
    for i in range(n_bins):
        magnitude += i*current_gaussian[i]

    # Normalize Gaussian
    current_gaussian /= current_sum
    stmt = gaussiansTable.update().where(gaussiansTable.c.cid==int(cid)).where(gaussiansTable.c.has_occupancy==True).values(emdvalue=magnitude)
    conn.execute(stmt)
    return current_gaussian


def calculateGaussianForCwout(cid):
    '''
    Computes the EMD Gaussian for a given cluster without parking data
    :param cid:
    :return: the resulting EMD Gaussian, as array
    '''
    amenitiesForClustersWout = pd.read_sql_query("""SELECT c.cid,
                                                               a.name,
                                                               c.dimvalue,
                                                               a.mean_duration,
                                                               a.stdev_duration
                                                        FROM cluster_emd_gaussians c
                                                        INNER JOIN amenities a ON c.dimname = a.name
                                                        WHERE NOT c.has_occupancy AND c.cid = """ + str(cid) + """
                                                        ORDER BY a.name""", engine)
    current_sum = 0
    current_gaussian = np.zeros((n_bins))
    for index, row in amenitiesForClustersWout.iterrows():
        if row['stdev_duration'] == 0 or np.isnan(row['stdev_duration']):
            continue
        current_sum += row['dimvalue']
        #current_gaussian += row['dimvalue'] * ot.datasets.get_1D_gauss(n_bins,
        #                                                               m=offset + row['mean_duration'],
        #                                                               s=row['stdev_duration'])
        current_gaussian += row['dimvalue'] * ot.datasets.make_1D_gauss(n_bins,
                                                                       m = offset + row['mean_duration'],
                                                                       #m = row['mean_duration'],
                                                                       s = row['stdev_duration'])

    # Normalize gaussian
    current_gaussian /= current_sum

    magnitude = 0
    for i in range(n_bins):
        magnitude += i*current_gaussian[i]

    stmt = gaussiansTable.update().where(gaussiansTable.c.cid==int(cid)).where(gaussiansTable.c.has_occupancy==False).values(emdvalue=magnitude)
    conn.execute(stmt)

    return current_gaussian


def calculateDistance(gaussianMap1, has1, gaussianMap2, has2):
    '''
    Calculates distance between two sets EMD Gaussians, either representing clusters with parking or clusters without
     parking data. The results is saved in the database.

    :param gaussianMap1:
    :param has1: boolean, whether gaussianMap1 contains Gaussians for clusters with parking data or not
    :param gaussianMap2:
    :param has2: boolean, whether gaussianMap2 contains Gaussians for clusters with parking data or not
    :return:
    '''
    for cid1 in gaussianMap1.keys():
        for cid2 in gaussianMap2.keys():
            if has1 == has2 and cid1 == cid2:
                continue
            if has1 == has2 and cid1 > cid2:
                continue

            gaussian1 = gaussianMap1[cid1]
            gaussian2 = gaussianMap2[cid2]
            #result = emd(gaussian1, gaussian2, distance_matrix, extra_mass_penalty=0)
            print('EMD between clusters id (' + str(cid1) + ', ' + str(cid2) + ') is ')
            result = wasserstein_distance(list(range(len(gaussian1))), list(range(len(gaussian2))),
                                                    u_weights = gaussian1, v_weights = gaussian2)
            result_norm = result * 100 / emd_max
            print('Distance is ' + str(round(result, 5)) + ' units (normalized: ' + str(round(result_norm, 5)) + '%)')

            stmt = similarityTable.insert().values(cid1 = int(cid1), has1 = has1, cid2 = int(cid2), has2 = has2,
                                                   similarity=round(result_norm, 2), simtype='emd')
            conn.execute(stmt)

            if has1 == has2:
                stmt = similarityTable.insert().values(cid1 = int(cid2), has1 = has1, cid2 = int(cid1), has2 = has2,
                                                       similarity=round(result_norm, 2), simtype='emd')
                conn.execute(stmt)
            else:
                stmt = similarityTable.insert().values(cid1 = int(cid2), has1 = has2, cid2 = int(cid1), has2 = has1,
                                                       similarity=round(result_norm, 2), simtype='emd')
                conn.execute(stmt)


if __name__ == "__main__":
    server = SSHTunnelForwarder('cloud31.dbis.rwth-aachen.de', ssh_username="ionita", ssh_password="andigenu", remote_bind_address=('127.0.0.1', 5432))
    server.start()
    engine = sqlalchemy.create_engine('postgres://aionita:andigenu@localhost:' + str(server.local_bind_port) + '/sfpark')
    conn = engine.connect()
    metadata = MetaData(engine)
    similarityTable = Table('cluster_similarity', metadata, autoload=True)
    gaussiansTable = Table('cluster_emd_gaussians', metadata, autoload=True)

    # Retrieving the bordering values for all Gaussians
    limits = pd.read_sql_query("SELECT MAX(mean_duration), MIN(mean_duration), MAX(stdev_duration) FROM amenities", engine)
    #limits = pd.read_sql_query("SELECT MIN(mean_duration - 3 * stdev_duration), MAX(mean_duration + 3 * stdev_duration), MAX(mean_duration), MIN(mean_duration) FROM amenities", engine)

    # Adding an offset to all discrete Gaussians representations
    # 3*stdev encompasses 99.5% of a normal distribution curve
    offset = 3 * limits.iloc[0][1]
    #if limits.iloc[0][0] < 0:
    #    offset = -1 * limits.iloc[0][0]
    #else:
    #    offset = 0
    n_bins = offset + limits.iloc[0][0]
    #n_bins = offset + limits.iloc[0][0] + 3 * limits.iloc[0][2]
    #n_bins = offset + limits.iloc[0][1]
    #n_bins = limits.iloc[0][1]
    # Calculating the maximum EMD
    emd_max = limits.iloc[0][0] - limits.iloc[0][1]
    #emd_max = limits.iloc[0][2] - limits.iloc[0][3]

    print('Number of bins: ' + str(n_bins))

    # Initializing the discrete Gaussian reprezantation
    x = np.arange(n_bins, dtype=np.float64)

    print('Calculting Gaussians for the Clusters with Data...')
    cwith_ids = pd.read_sql_query("""SELECT DISTINCT ON (cid) cid FROM cluster_emd_gaussians WHERE has_occupancy;""",
                                  engine)
    gaussianMapWith = {}
    for index, row in cwith_ids.iterrows():
        cwithid = row['cid']
        gaussianMapWith[cwithid] = calculateGaussianForCwith(cwithid)
        #print('cwithid ' + str(cwithid))
        #print(gaussianMapWith[cwithid])

    print('Calculting Gaussians for the Clusters without Data...')
    cwout_ids = pd.read_sql_query("""SELECT DISTINCT ON (cid) cid FROM cluster_emd_gaussians
                                    WHERE NOT has_occupancy;""", engine)
    gaussianMapWout = {}
    for index, row in cwout_ids.iterrows():
        cwoutid = row['cid']
        gaussianMapWout[cwoutid] = calculateGaussianForCwout(cwoutid)
        #print('cwoutid ' + str(cwoutid))
        #print(gaussianMapWout[cwoutid])


    # Calculate distance matrix, necessary for calculating EMDs
    distance_matrix = np.zeros((n_bins, n_bins))
    for i in range(n_bins):
        for j in range(n_bins):
            distance_matrix[i][j] = abs(i - j)

    print('-------------------------------------------------------')
    print('Clusters WITH Parking Data : Clusters WITH Parking Data')
    print('-------------------------------------------------------')
    calculateDistance(gaussianMapWith, True, gaussianMapWith, True)

    print('----------------------------------------------------------')
    print('Clusters WITH Parking Data : Clusters WITHOUT Parking Data')
    print('----------------------------------------------------------')
    calculateDistance(gaussianMapWith, True, gaussianMapWout, False)

    print('-------------------------------------------------------------')
    print('Clusters WITHOUT Parking Data : Clusters WITHOUT Parking Data')
    print('-------------------------------------------------------------')
    calculateDistance(gaussianMapWout, False, gaussianMapWout, False)

    server.stop()
