#!/bin/bash

IMAGE_NAME=bvnordic/osm-convert
TMP_DIR=/data/osm-conversion/tmpdata
TMP_JOINED=$TMP_DIR/joined.geojson
TRANSLATIONS_DIR=/data/osm-conversion/translation

cd `dirname $0`
docker build -t $IMAGE_NAME .

docker run --rm -w /data -v $PWD/..:/data $IMAGE_NAME ogr2ogr -sql "SELECT t.geom, t.dog_friend AS dog_friend, t.lights AS lights, t.difficulty AS difficulty, tn.trail_name AS name FROM trails t JOIN trail_names tn ON t.trail_id = tn.trail_id" $TMP_JOINED main-data.gpkg

docker run --rm -v $PWD/..:/data $IMAGE_NAME /source/ogr2osm/ogr2osm.py $TMP_JOINED -f -o $TMP_DIR/out.osm -t $TRANSLATIONS_DIR/nordic_tags.py
EXIT_CODE=$?

if [[ -z $RETAIN_INTERMEDIARIES || $RETAIN_INTERMEDIARIES == "0" ]]; then
    docker run --rm -v $PWD/..:/data $IMAGE_NAME rm $TMP_JOINED
fi

exit $EXIT_CODE
