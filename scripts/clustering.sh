#!/bin/bash

if [[ $# -eq 0 ]] ; then
	echo "Please provide the number of clusters for the areas with parking data"
	exit
fi

python workspace/parking-estimator/src/clustering/ClusterKMeans.py $1
