#!/bin/bash

osmium renumber -o /output/bvnordic-renumbered.osm /output/bvnordic.osm

service postgresql start
while ! nc -z localhost 5432; do echo "postgres not yet ready"; sleep 1; done;

createdb gis
psql -d gis -c "CREATE EXTENSION postgis; CREATE EXTENSION hstore;"

PGPASSWORD=postgres osm2pgsql -U postgres -d gis --hstore -G --style /source/openstreetmap-carto/openstreetmap-carto.style --tag-transform-script /source/openstreetmap-carto/openstreetmap-carto.lua /output/bvnordic-renumbered.osm

pushd /source/openstreetmap-carto/
carto project.mml > osm.xml
./scripts/get-external-data.py

MAPNIK_MAP_FILE=$PWD/osm.xml python3 /generate_image.py

ls -Alh