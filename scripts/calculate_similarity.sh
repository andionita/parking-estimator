#!/bin/bash

echo
echo "-------------------------------------------------"
echo "Calculating Cosine Similarity between clusters..."
psql -U andio -h localhost -f ~/parking-estimator_git/scripts/clustering_process_2cosine.sql sfpark


echo
echo "-------------------------------------------------"
echo "Calculating Earth Mover's Distance between clusters..."
psql -U andio -h localhost -f ~/parking-estimator_git/scripts/clustering_process_2a_emd.sql sfpark

python3 workspace/parking-estimator/src/emd/AmenityEMD.py

#echo
#echo "-------------------------------------------------"
#echo "Exporting results to JSON..."
#psql -U andio -h localhost -f ~/parking-estimator_git/scripts/clustering_process_3tojson.sql sfpark"

#sh scripts/copy_as_javascript.sh . leaflet/js clusters_wout

#sh scripts/copy_as_javascript.sh . leaflet/js clusters_with
