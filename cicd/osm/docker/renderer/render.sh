#!/bin/bash

service postgresql start
while ! nc -z localhost 5432; do echo "postgres not yet ready"; sleep 1; done;

createdb gis
psql -d gis -c "CREATE EXTENSION postgis; CREATE EXTENSION hstore;"

osmium renumber -o bvnordic-loader.osm /code/output/bvnordic.osm
PGPASSWORD=postgres osm2pgsql -U postgres -d gis --hstore -G bvnordic-loader.osm

carto /code/cicd/osm/docker/renderer/styles/trails.mml > trails.xml

ogr2ogr -f GeoJSON -t_srs "EPSG:4326" -dialect sqlite -sql "SELECT ST_Envelope(ST_Buffer(ST_Envelope(ST_Union(geom)), 100)) FROM Trails" extent.json /code/main-data.gpkg
EXTENT=$(cat extent.json | jq -r '.features[0].geometry.coordinates[0] | "\(.[0][0]) \(.[0][1]) \(.[2][0]) \(.[2][1])"')

MAP_FILE=$PWD/trails.xml
pushd /code
MAPNIK_MAP_FILE=$MAP_FILE EXTENT=$EXTENT OUTPUT_PNG_PATH=/code/output/output.png python3 -m cicd.osm.docker.renderer.generate_image
