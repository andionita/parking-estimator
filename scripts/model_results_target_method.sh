# Formatting the psql \copy statement, which otherwhise doesn't allow variable subsitution

# Exporting Machine Learning Model results based on target Clusters 
# Exporting Models for a given Method (e.g. dt, svm, mlp, xgb). Attributes included:
#  target cluster id
#  model name
#  training error
#  source cluster id
#  similarity between target and source
#  test error

printf "\COPY (SELECT json_build_object('type' , 'FeatureCollection', 'features', json_agg(json_build_object('type' , 'Feature', 'similar_clusterid' , similar_clusterid, 'properties', json_build_object('model_names', model_names, 'training_errors', training_errors, 'clusterids', clusterids, 'similarities', similarities, 'simtypes', simtypes, 'errors', errors)))) FROM (SELECT similar_clusterid, array_agg(model_name) AS model_names, array_agg(training_error) AS training_errors, array_agg(clusterid) AS clusterids, array_agg(similarity) AS similarities, array_agg(simtype) AS simtypes, array_agg(error) AS errors FROM models m1 LEFT JOIN cluster_similarity cs ON m1.similar_clusterid = cs.cid1 AND m1.clusterid = cs.cid2 AND has1 AND has2 WHERE m1.clusterid <= (SELECT MAX(cwithid) FROM blocks) AND m1.similar_clusterid <= (SELECT MAX(cwithid) FROM blocks) AND run_timestamp = (SELECT MAX(run_timestamp) FROM models m2 WHERE m1.similar_clusterid = m2.similar_clusterid AND m1.clusterid = m2.clusterid) AND model_name = '%s' GROUP BY similar_clusterid) AS aux) TO 'model_results_target_method_%s.json';" $1 $1
