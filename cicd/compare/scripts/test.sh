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

GITHUB_SHA=$(uuidgen)

cicd/compare/scripts/check_comparable.sh before=$BEFORE after=$AFTER
. cicd/compare/scripts/create_directories.sh before=$BEFORE after=$AFTER

UPLOAD_IF_MISSING=0
if [ "$CI" == "true" ]; then
    UPLOAD_IF_MISSING=1
fi
cicd/scripts/pull_or_build.sh repo=tomfumb image=qgis-exporter:2 build_dir=cicd/export/docker context_dir=cicd upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -e REVISION=$BEFORE -v $PWD:/code tomfumb/qgis-exporter:2 /workdir/cicd/export/docker/generate.sh output_base=/code/$OUTPUT_BASE/$BEFORE png=1
docker run --rm -e REVISION=$AFTER  -v $PWD:/code tomfumb/qgis-exporter:2 /workdir/cicd/export/docker/generate.sh output_base=/code/$OUTPUT_BASE/$AFTER png=1

GITHUB_SHA=$GITHUB_SHA cicd/osm/scripts/export.sh local_output_dir=$OUTPUT_BASE/$BEFORE revision=$BEFORE
GITHUB_SHA=$GITHUB_SHA cicd/osm/scripts/export.sh local_output_dir=$OUTPUT_BASE/$AFTER revision=$AFTER

cicd/scripts/pull_or_build.sh repo=tomfumb image=bvnordic-osm-renderer:2 build_dir=cicd/osm/docker/renderer context_dir=cicd upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -e REVISION=$BEFORE -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 /workdir/cicd/osm/docker/renderer/render.sh data_dir=/code/$OUTPUT_BASE/$BEFORE/main
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdalwarp -ts 1600 0 /code/cicd/imagery/output/network.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.tif
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdal_translate -of PNG -co zlevel=9 /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.png
docker run --rm -e REVISION=$AFTER  -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 /workdir/cicd/osm/docker/renderer/render.sh data_dir=/code/$OUTPUT_BASE/$AFTER/main
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdalwarp -ts 1600 0 /code/cicd/imagery/output/network.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.tif
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdal_translate -of PNG -co zlevel=9 /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.png

python -m cicd.compare.detect_changes $BEFORE $AFTER $PWD/$OUTPUT_BASE

rm -rf $OUTPUT_BASE/$BEFORE
rm -rf $OUTPUT_BASE/$AFTER

if [ "$UPLOAD" == "1" ]; then
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO python -m cicd.upload.upload $COMPARE_DIR $PWD/output
fi