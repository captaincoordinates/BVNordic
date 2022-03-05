#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            upload) UPLOAD=${VALUE} ;;
            *)   
    esac    
done

pushd $(dirname $0)/../../..


GITHUB_SHA=$(uuidgen)
GITHUB_SHA=$GITHUB_SHA EXPORT_DIR_PREFIX=test- . cicd/export/scripts/create_directory.sh

UPLOAD_IF_MISSING=0
if [ "$CI" == "true" ]; then
    UPLOAD_IF_MISSING=1
fi
cicd/scripts/pull_or_build.sh repo=tomfumb image=qgis-exporter:2 build_dir=cicd/export/docker context_dir=cicd upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -v $PWD:/code -e SHORTCUT_FOR_TESTING tomfumb/qgis-exporter:2 /workdir/cicd/export/docker/generate.sh output_base=/code/$LOCAL_OUTPUT_DIR pdf=1

GITHUB_SHA=$GITHUB_SHA cicd/osm/scripts/export.sh local_output_dir=$LOCAL_OUTPUT_DIR

if [ "$UPLOAD" == "1" ]; then
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_CI_UPLOAD_SERVICE_ACCT_INFO python -m cicd.upload.upload $UNIQUE_DIR $PWD/output
fi