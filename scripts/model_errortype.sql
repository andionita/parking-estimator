-- Export the Error Type for Machine Learning model testing
-- The value is taken from the last training round
-- Attributes included:
--		error type

\COPY (SELECT json_build_object('error_type', error_type) FROM (SELECT error_type FROM models m1 WHERE run_timestamp = (SELECT MAX(run_timestamp) FROM models m2 WHERE m1.clusterid = m2.clusterid) LIMIT 1) AS aux) TO 'model_errortype.json';
