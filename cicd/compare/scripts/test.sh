#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            before) BEFORE=${VALUE} ;;
            after)  AFTER=${VALUE} ;;     
            *)   
    esac    
done

pushd $(dirname $0)/../../..

cicd/compare/scripts/check_comparable.sh before=$BEFORE after=$AFTER
. cicd/compare/scripts/create_directories.sh before=$BEFORE after=$AFTER

docker build -t exporter cicd/export/docker
docker run --rm -v $PWD:/code exporter /code/cicd/export/docker/generate_revision.sh output_base=/code/$OUTPUT_BASE/$BEFORE revision=$BEFORE
docker run --rm -v $PWD:/code exporter /code/cicd/export/docker/generate_revision.sh output_base=/code/$OUTPUT_BASE/$AFTER revision=$AFTER

python -m cicd.compare.detect_changes $BEFORE $AFTER $PWD/$OUTPUT_BASE

cicd/compare/scripts/remove_directories.sh output_base=$OUTPUT_BASE before=$BEFORE after=$AFTER

# upload.sh in current form may be layout-specific with --update_latest parameter. This concept is not relevant for comparisons
# if [ "$3" == "1" ]; then
#     UPLOAD_ROOT=$PWD/output
#     pushd upload
#     GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO python -m src.upload $COMPARE_DIR $UPLOAD_ROOT
#     popd
# fi