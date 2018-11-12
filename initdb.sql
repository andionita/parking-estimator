DROP TABLE IF EXISTS blocks;
CREATE TABLE blocks (
    wkt geometry(Geometry),
    objectid integer,
    block_id real,
    area_type character varying(25),
    pm_district real,
    block_num real,
    street_id real,
    street_name character varying(25),
    fm_addr_no real,
    to_addr_no real,
    shape_leng double precision,
    shape_area double precision
);

\copy blocks FROM 'osm/SFpark_Blocks.csv' DELIMITER ',' CSV HEADER

-- set CRS for geometry afterwards, as it did not have any CRS in CSV format
SELECT UpdateGeometrySRID('blocks','wkt',4326);

DROP TABLE IF EXISTS occupancy;

CREATE TABLE occupancy (
        block_id integer,
        street_name varchar(30),
        block_num integer,
        street_block varchar(30),
        area_type varchar(10),
        district_name varchar(30),
        price_rate real,
        timestamp timestamp,
        day_type varchar(10),
        total_spots integer,
        occupied real
);

\copy occupancy FROM 'sfpark/tuned_occupancy_030917_final.csv' DELIMITER ',' CSV HEADER

ALTER TABLE blocks ADD COLUMN has_occupancy boolean;

UPDATE blocks b
SET has_occupancy = TRUE
FROM
  (SELECT array_agg(distinct(b.block_id)) AS list
   FROM blocks b
   INNER JOIN occupancy o ON b.block_id = o.block_id) AS TEMP
WHERE b.block_id = ANY(TEMP.list);

UPDATE blocks SET has_occupancy = false where has_occupancy is null;

ALTER TABLE blocks ADD COLUMN cwithid integer;
ALTER TABLE blocks ADD COLUMN cwoutid integer;

-- fix some broken geometries, if need be
UPDATE blocks SET wkt=ST_makevalid(wkt) WHERE NOT ST_isValid(wkt);

ALTER TABLE blocks ADD COLUMN occupancy_points integer;

UPDATE blocks b
SET occupancy_points = aux.occupancy_points
FROM
  (SELECT block_id,
          count(*) AS occupancy_points
   FROM occupancy
   GROUP BY block_id) AS aux
WHERE b.block_id = aux.block_id;

CREATE TABLE poi_reduced AS
SELECT poi.osm_id as poi_osm_id, poi.name as poi_name, poi.amenity as poi_amenity, poi.tags -> 'addr:street' as poi_street, 
    poi.tags -> 'addr:housenumber' as poi_housenumber, poi.tags -> 'capacity' as poi_capacity, 
    poi.tags -> 'description' as poi_description, 
    poi.tags -> 'level' as poi_level, poi.tags -> 'opening_hours' as poi_opening_hours, 
    poi.tags -> 'parking' as poi_parking, st_transform(poi.way, 4326) as poi_geom
    FROM planet_osm_point poi WHERE poi.amenity != '';

-- set CRS for geometries
SELECT UpdateGeometrySRID('poi_reduced','poi_geom',4326);
SELECT UpdateGeometrySRID('blocks','wkt',4326);

-- create and populate table that merges blocks with the osm poi_polygon table
CREATE TABLE merge_block_poi AS (SELECT b.block_id as block_id, temp.poi_osm_id as osm_id, temp.poi_amenity as amenity, temp.poi_geom as geom FROM blocks b 
                              INNER JOIN (SELECT DISTINCT poi_osm_id, poi_amenity, poi_geom FROM poi_reduced WHERE poi_amenity IS NOT NULL) as temp 
                              ON ST_Distance(b.wkt, temp.poi_geom) < 0.001 ORDER BY b.block_id, temp.poi_osm_id);

CREATE TABLE cluster_cosine_vectors (
	cid integer,
	has_occupancy boolean,
	dimid integer,
	dimvalue bigint
);

CREATE TABLE cluster_emd_gaussians (
	cid integer,
	has_occupancy boolean,
	dimname varchar(50),
	dimvalue bigint,
	emdvalue double precision
);

CREATE TABLE amenities (
	name varchar(40),
	mean_duration integer,
	stdev_duration integer,
	category integer
);

\copy amenities FROM 'scripts/csvs/amenities_min2sources_categoriesV2.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE cluster_similarity (
	cid1 integer,
	cid2 integer,
	has1 boolean,
	has2 boolean,
	similarity numeric,
	simtype varchar(20)
);

CREATE TABLE models (
	clusterid integer,
	data_points integer,
	run_timestamp timestamp,
	similar_clusterid integer,
	model_name varchar(10),
	error real,
	error_type varchar(10),
	training_time integer,
	training_error real
);
