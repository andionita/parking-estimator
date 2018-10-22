# Exporting Machine Learning model results based on target Clusters  
# Exporting Models that give the best test results for a target - source cluster pair. Attributes included:
#      target cluster id
#      model name
#      training error
#      source cluster id
#      similarity between target and source
#	   similarity type, e.g. cosine or emd
#      test error

printf "\COPY (SELECT json_build_object('type' , 'FeatureCollection', 'features', json_agg(json_build_object('type' , 'Feature', 'similar_clusterid' , similar_clusterid, 'properties', json_build_object('model_names', model_names, 'training_errors', training_errors, 'clusterids', clusterids, 'errors', errors, 'similarities', similarities, 'simtypes', simtypes)))) FROM (SELECT similar_clusterid, array_agg(model_name) AS model_names, array_agg(training_error) AS training_errors, array_agg(clusterid) AS clusterids, array_agg(similarity) AS similarities, array_agg(simtype) AS simtypes, array_agg(error) AS errors FROM models m1 LEFT JOIN cluster_similarity cs ON m1.similar_clusterid = cs.cid1 AND m1.clusterid = cs.cid2 AND has1 AND has2 WHERE m1.clusterid <= (SELECT MAX(cwithid) FROM blocks) AND m1.similar_clusterid <= (SELECT MAX(cwithid) FROM blocks) AND run_timestamp = (SELECT MAX(run_timestamp) FROM models m2 WHERE m1.similar_clusterid = m2.similar_clusterid AND m1.clusterid = m2.clusterid) AND error = (SELECT MIN(error) FROM models m3 WHERE m3.run_timestamp = m1.run_timestamp AND m3.similar_clusterid = m1.similar_clusterid AND m3.clusterid = m1.clusterid) GROUP BY similar_clusterid) AS aux) TO 'model_results_target_method_best.json';"
