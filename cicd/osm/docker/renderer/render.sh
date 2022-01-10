#!/bin/bash

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            data_dir) DATA_DIR=${VALUE} ;;
            *)
    esac    
done

service postgresql start
while ! nc -z localhost 5432; do echo "postgres not yet ready"; sleep 1; done;

createdb -U postgres gis
psql -U postgres -d gis -c "CREATE EXTENSION postgis; CREATE EXTENSION hstore;"

osmium renumber -o bvnordic-loader.osm $DATA_DIR/bvnordic.osm
PGPASSWORD=postgres osm2pgsql -U postgres -d gis --hstore -G bvnordic-loader.osm

carto /code/cicd/osm/docker/renderer/styles/segments.mml > segments.xml
carto /code/cicd/osm/docker/renderer/styles/routes.mml > routes.xml

BUFFER_QUERY="'SELECT ST_Envelope(ST_Buffer(ST_Envelope(ST_Union(geom)), 100)) FROM Trails'"

ogr2ogr -f GeoJSON -t_srs "EPSG:4326" -dialect sqlite -sql $BUFFER_QUERY 4326.json /code/main-data.gpkg
ogr2ogr -f GeoJSON -dialect sqlite -sql $BUFFER_QUERY native.json /code/main-data.gpkg

EXTENT=$(cat 4326.json | jq -r '.features[0].geometry.coordinates[0] | "\(.[0][0]) \(.[0][1]) \(.[2][0]) \(.[2][1])"')

MAP_FILE_DIR=$PWD
pushd /code
MAPNIK_MAP_FILE=$MAP_FILE_DIR/segments.xml EXTENT=$EXTENT OUTPUT_PNG_PATH=$DATA_DIR/bvnordic.osm-segments.png python3 -m cicd.osm.docker.renderer.generate_image
MAPNIK_MAP_FILE=$MAP_FILE_DIR/routes.xml EXTENT=$EXTENT OUTPUT_PNG_PATH=$DATA_DIR/bvnordic.osm-routes.png python3 -m cicd.osm.docker.renderer.generate_image

cat $MAP_FILE_DIR/native.json

# gdal_translate -of GTIFF -a_ullr