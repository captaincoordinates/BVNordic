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

GITHUB_SHA="test-$(uuidgen)" . cicd/export/scripts/create_directory.sh

docker build -t exporter cicd/export/docker
docker run --rm -v $PWD:/code exporter /code/cicd/export/docker/generate_head.sh output_base=/code/$LOCAL_OUTPUT_DIR png=1 pdf=1

cicd/osm/scripts/osm.sh local_output_dir=$LOCAL_OUTPUT_DIR

if [ "$UPLOAD" == "1" ]; then
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_CI_UPLOAD_SERVICE_ACCT_INFO python -m cicd.upload.upload $UNIQUE_DIR $PWD/output
fi