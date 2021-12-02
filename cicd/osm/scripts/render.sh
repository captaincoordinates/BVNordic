#!/bin/bash

pushd $(dirname $0)/../../..

UPLOAD_IF_MISSING=0
if [ "$CI" == "true" ]; then
    UPLOAD_IF_MISSING=1
fi
cicd/scripts/pull_or_build.sh repo=tomfumb image=bvnordic-osm-renderer:1 build_dir=cicd/osm/docker/renderer context_dir=cicd/osm upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm \
    -v $PWD:/code \
    tomfumb/bvnordic-osm-renderer:1 \
    /code/cicd/osm/docker/renderer/render.sh