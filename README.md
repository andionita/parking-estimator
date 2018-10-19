Workflow for setting up and running the parking-estimator application
======================================================================
By default, all statements in this file are executed from the root directory.
Be aware that some scripts need your database username in order to run. This will be pointed out throughout this tutorial. 
Please edit the files and replace the username with yours.

Prerequisites:
--------------
- Python 2
- PostGRESQL with POSTGIS extensions
- Java 8
- osm2pgsql


The input data is the following:
--------------------------------
- Parking data
--- blocks data from SFpark: osm/SFpark_Blocks.csv
--- occupancy data from SFpark: sfpark/tuned_occupancy_030917_final.csv
--- traffic data from SFpark: sfpark/traffic_by_district.csv (not used)

- City data
--- POI and other layers from OSM: osm/osm_sfpark_blocks.osm
--- amenity data from Google: scripts/csvs/amenities_min2sources_categoriesV2.csv


Setup
-----
1. Execute "CREATE DATABASE sfpark WITH OWNER <your_username>;" in psql to create the database sfpark for your username. Add extensions "CREATE EXTENSION postgis;" and "CREATE EXTENSION hstore;" for sfpark.

2. Execute "scripts/import_osm_into_postgis.sh" to import city data into the database using osm2pgsql.
NOTE! Please introduce your own database user in the script before executing it.

3. Execute "initdb.sql" in psql to initialize database tables.
psql -f initdb.sql -U <your_username> -h localhost sfpark
 
Building cycle
-------------- 
1. Cluster the city areas into 8 clusters with parking data and 20 clusters without parking data.
scripts/clustering.sh 8

2. Calculate similarity values for the clusters (both cosine similarity and emd).
scripts/calculate_similarity.sh

3. Build machine learning models for the clusters with parking data.
NOTE! Please introduce your own database user in the script before executing it.
scripts/train_and_test.sh
