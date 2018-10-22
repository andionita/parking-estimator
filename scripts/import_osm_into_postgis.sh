#!/bin/bash
export OSM_CREATE='osm2pgsql -k -c -d sfpark -U andio -H localhost -W'

# extract from OSM file
$OSM_CREATE osm/osm_sfpark_blocks.osm
