#!/bin/bash

set -e

pushd $(dirname $0)/..

IMAGE_NAME=bvnordic/osm-convert
OUT_DIR=/data/$LOCAL_OUTPUT_DIR
TMP_JOINED=$OUT_DIR/joined.geojson
TRANSLATIONS_DIR=/data/osm-conversion/translation

docker build -t $IMAGE_NAME osm-conversion

docker run --rm -w /data -v $PWD:/data $IMAGE_NAME ogr2ogr -sql "SELECT t.geom, t.dog_friend AS dog_friend, t.lights AS lights, t.difficulty AS difficulty, tn.trail_name AS name FROM trails t JOIN trail_names tn ON t.trail_id = tn.trail_id" $TMP_JOINED main-data.gpkg

docker run --rm -v $PWD:/data $IMAGE_NAME /source/ogr2osm/ogr2osm.py $TMP_JOINED -f -o $OUT_DIR/bvnordic.osm -t $TRANSLATIONS_DIR/nordic_tags.py
EXIT_CODE=$?

docker run --rm -v $PWD:/data $IMAGE_NAME rm $TMP_JOINED

exit $EXIT_CODE
