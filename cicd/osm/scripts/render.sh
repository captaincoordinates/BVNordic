#!/bin/bash

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

UPLOAD_IF_MISSING=0
if [ "$CI" == "true" ]; then
    UPLOAD_IF_MISSING=1
fi
cicd/scripts/pull_or_build.sh repo=tomfumb image=bvnordic-osm-renderer:1 build_dir=cicd/osm/docker/renderer context_dir=cicd/osm upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm \
    -v $PWD:/code \
    -p 5432:5432 \
    tomfumb/bvnordic-osm-renderer:1 \
    /code/cicd/osm/docker/renderer/render.sh data_dir=/code/$LOCAL_OUTPUT_DIR/main