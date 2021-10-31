#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            before) BEFORE=${VALUE} ;;
            after)  AFTER=${VALUE} ;;
            upload) UPLOAD=${VALUE} ;;
            *)   
    esac    
done

pushd $(dirname $0)/../../..

cicd/compare/scripts/check_comparable.sh before=$BEFORE after=$AFTER
. cicd/compare/scripts/create_directories.sh before=$BEFORE after=$AFTER

docker build -t exporter cicd/export/docker
docker run --rm -v $PWD:/code exporter /code/cicd/export/docker/generate_revision.sh output_base=/code/$OUTPUT_BASE/$BEFORE revision=$BEFORE png=1
docker run --rm -v $PWD:/code exporter /code/cicd/export/docker/generate_revision.sh output_base=/code/$OUTPUT_BASE/$AFTER revision=$AFTER png=1

python -m cicd.compare.detect_changes $BEFORE $AFTER $PWD/$OUTPUT_BASE

rm -rf $OUTPUT_BASE/$BEFORE
rm -rf $OUTPUT_BASE/$AFTER

if [ "$UPLOAD" == "1" ]; then
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO python -m cicd.upload.upload $COMPARE_DIR $PWD/output
fi