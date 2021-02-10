#!/bin/sh

IMAGE_NAME=bvnordic/osm-convert
TMP_DIR=/data/osm-conversion/tmpdata
TMP_JOINED=$TMP_DIR/joined.geojson

cd `dirname $0`
docker build -t $IMAGE_NAME .

docker run --rm -w /data -v $PWD/..:/data $IMAGE_NAME ogr2ogr -sql "select trails.dog_friend as dog_friend, trails.lights as lights, trails.difficulty as difficulty, trail_names.trail_name as name from trails join 'trail_names.csv'.trail_names on trails.trail_id = trail_names.trail_id" $TMP_JOINED trails.shp

docker run --rm -v $PWD/..:/data $IMAGE_NAME /source/ogr2osm/ogr2osm.py $TMP_JOINED -f -o $TMP_DIR/out.osm
EXIT_CODE=$?

docker run --rm -v $PWD/..:/data $IMAGE_NAME rm $TMP_JOINED


exit $EXIT_CODE
