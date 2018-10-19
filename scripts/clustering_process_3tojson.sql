-- For every source Cluster without Parking Data export target Clusters with Parking Data (cwout : cwith)

-- Source Cluster attributes:
-- cwoutid
-- geometry

-- Target Clusters attributes:
-- similar_cwithids
-- similarities
-- similarity_types

\COPY (SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(json_build_object('type', 'Feature', 'geometry' , ST_AsGeoJSON(aux2.merged_geom)::json, 'properties', json_build_object('cwoutid', aux2.cwoutid, 'similar_cwithids', array_to_json(aux2.similar_cwithids), 'similarities', array_to_json(aux2.similarities), 'similarity_types', array_to_json(aux2.similarity_types))))) FROM (SELECT cwoutid, ST_UNION(wkt) AS merged_geom, aux.similar_cwithids AS similar_cwithids, aux.similarities AS similarities, aux.similarity_types AS similarity_types FROM blocks INNER JOIN (SELECT cid1, array_agg(cid2 ORDER BY similarity DESC) AS similar_cwithids, array_agg(round(similarity,7) ORDER BY similarity DESC) AS similarities, array_agg(simtype ORDER BY similarity DESC) AS similarity_types FROM cluster_similarity WHERE NOT has1 AND has2 GROUP BY cid1) AS aux ON aux.cid1 = blocks.cwoutid WHERE NOT has_occupancy GROUP BY cwoutid, aux.similar_cwithids, aux.similarities, aux.similarity_types) AS aux2) TO 'clusters_wout.json';


-- For every source Cluster with Parking Data export target Clusters with Parking Data (cwith : cwith)

-- Source Cluster attributes:
-- cwithid
-- geometry

-- Target Clusters attributes:
-- occupancy_points
-- similar_cwithids
-- similarities
-- similarity_types

\COPY (SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(json_build_object('type', 'Feature', 'geometry' , ST_AsGeoJSON(aux2.merged_geom)::json, 'properties', json_build_object('cwithid', aux2.cwithid, 'occupancy_points', aux2.occupancy_points, 'similar_cwithids', array_to_json(aux2.similar_cwithids), 'similarities', array_to_json(aux2.similarities), 'similarity_types', array_to_json(aux2.similarity_types))))) FROM (SELECT cwithid, SUM(occupancy_points) AS occupancy_points, ST_UNION(wkt) AS merged_geom, aux.similar_cwithids AS similar_cwithids, aux.similarities AS similarities, aux.similarity_types AS similarity_types FROM blocks INNER JOIN (SELECT cid1, array_agg(cid2 ORDER BY similarity DESC) AS similar_cwithids, array_agg(round(similarity,7) ORDER BY similarity DESC) AS similarities, array_agg(simtype ORDER BY similarity DESC) AS similarity_types FROM cluster_similarity WHERE has1 AND has2 GROUP BY cid1) AS aux ON aux.cid1 = blocks.cwithid WHERE has_occupancy GROUP BY cwithid, aux.similar_cwithids, aux.similarities, aux.similarity_types) AS aux2) TO 'clusters_with.json';
