#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            local_output_dir) LOCAL_OUTPUT_DIR=${VALUE} ;;
            *)   
    esac    
done

pushd $(dirname $0)/../../..

DOCKER_REPO=tomfumb
DOCKER_IMAGE=bvnordic-osm-exporter
DOCKER_TAG=$DOCKER_REPO/$DOCKER_IMAGE
OUT_DIR=/data/$LOCAL_OUTPUT_DIR
TMP_JOINED=$OUT_DIR/joined.geojson
TRANSLATIONS_DIR=/data/cicd/osm/translation

UPLOAD_IF_MISSING=0
if [ "$CI" == "true" ]; then
    UPLOAD_IF_MISSING=1
fi
cicd/scripts/pull_or_build.sh repo=$DOCKER_REPO image=$DOCKER_IMAGE build_dir=cicd/osm/docker context_dir=cicd/osm upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -w /data -v $PWD:/data $DOCKER_TAG ogr2ogr -sql "SELECT t.geom, t.dog_friend AS dog_friend, t.lights AS lights, t.difficulty AS difficulty, tn.trail_name AS name FROM trails t JOIN trail_names tn ON t.trail_id = tn.trail_id" $TMP_JOINED main-data.gpkg

docker run --rm -v $PWD:/data -e GITHUB_SHA $DOCKER_TAG ogr2osm $TMP_JOINED -f -o $OUT_DIR/bvnordic-partial.osm -t $TRANSLATIONS_DIR/nordic_tags.py
EXIT_CODE=$?

python -m cicd.osm.routes $LOCAL_OUTPUT_DIR/bvnordic-partial.osm $LOCAL_OUTPUT_DIR/bvnordic.osm

rm $LOCAL_OUTPUT_DIR/*.geojson
rm $LOCAL_OUTPUT_DIR/bvnordic-partial.osm

exit $EXIT_CODE
