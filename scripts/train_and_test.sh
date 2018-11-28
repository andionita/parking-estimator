#!/bin/bash

# Sample usage:
#   train_and_test.sh
#		models for all clusters will be trained
#   train_and_test.sh --skip-training
#		skips model training (persisted models will be used)
#   train_and_test.sh --all-datapoints
#               when building models do not aggregate datapoints per timestamp, instead use all occupancy data 


if [ "$1" != "--skip-training" ]; then
	echo "Starting to train the models..."
	if [ "$1" == "--all-datapoints" ]; then
		python workspace/parking-estimator/src/modeltraining/BestClusterSelectionAll.py --all-datapoints
	else
		python workspace/parking-estimator/src/modeltraining/BestClusterSelectionAll.py
	fi
else
	echo "Skipping model training"
fi

#echo "Exporting cluster ids and datapoints..."
#psql -U andio -h localhost -f scripts/cluster_datapoints.sql sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js cluster_datapoints
#echo "Exporting the current error type for machine learning model testing..."
#psql -U andio -h localhost -f scripts/model_errortype.sql sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_errortype

#echo "Exporting model results for Source Clusters for Decision Trees..."
#sh scripts/model_results_source_method.sh 'dt' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_source_method_dt
#echo "Exporting model results for Source Clusters for SVM..."
#sh scripts/model_results_source_method.sh 'svm' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_source_method_svm
#echo "Exporting model results for Source Clusters for MLP..."
#sh scripts/model_results_source_method.sh 'mlp' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_source_method_mlp
#echo "Exporting model results for Source Clusters for XGB..."
#sh scripts/model_results_source_method.sh 'xgb' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_source_method_xgb

#echo "Exporting model results for Source Clusters that have best results..."
#sh scripts/model_results_source_method_best.sh | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_source_method_best

#echo "Exporting model results for Target Clusters for Decision Trees..."
#sh scripts/model_results_target_method.sh 'dt' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_target_method_dt
#echo "Exporting model results for Target Clusters for SVM..."
#sh scripts/model_results_target_method.sh 'svm' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_target_method_svm
#echo "Exporting model results for Target Clusters for MLP..."
#sh scripts/model_results_target_method.sh 'mlp' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_target_method_mlp
#echo "Exporting model results for Target Clusters for XGB..."
#sh scripts/model_results_target_method.sh 'xgb' | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_target_method_xgb

#echo "Exporting model results for Target Clusters that have best results..."
#sh scripts/model_results_target_method_best.sh | psql -U andio -h localhost sfpark
#sh scripts/copy_as_javascript.sh . leaflet/js model_results_target_method_best

echo "Applying models for Clusters without Parking Data..."
if [ "$1" == "--all-datapoints" ]; then
	python workspace/parking-estimator/src/modeltraining/ModelPredictionCwout.py --all-datapoints
else
	python workspace/parking-estimator/src/modeltraining/ModelPredictionCwout.py
fi
#sh scripts/copy_as_javascript.sh workspace/parking-estimator/jsons leaflet/js estimations_cwout
