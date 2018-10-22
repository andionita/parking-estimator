-- Export the Clusters with Parking Data together with their Data Points
-- Data is taken from the last Model Training round
-- Attributes included:
--		clusterid
--		occupancy data points

\COPY (SELECT json_build_object('type' , 'FeatureCollection', 'features', json_agg(json_build_object('type' , 'Feature', 'clusterid', clusterid, 'data_points', data_points))) FROM (SELECT DISTINCT ON (clusterid) clusterid, data_points FROM models m1 WHERE run_timestamp = (SELECT MAX(run_timestamp) FROM models m2 WHERE m1.clusterid = m2.clusterid)) AS aux) TO 'cluster_datapoints.json';
