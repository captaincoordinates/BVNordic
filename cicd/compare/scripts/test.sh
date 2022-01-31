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

# export map layouts from each revision for pixel comparison
cicd/scripts/pull_or_build.sh repo=tomfumb image=qgis-exporter:2 build_dir=cicd/export/docker context_dir=cicd upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -e REVISION=$BEFORE -v $PWD:/code tomfumb/qgis-exporter:2 /workdir/cicd/export/docker/generate.sh output_base=/code/$OUTPUT_BASE/$BEFORE png=1
docker run --rm -e REVISION=$AFTER  -v $PWD:/code tomfumb/qgis-exporter:2 /workdir/cicd/export/docker/generate.sh output_base=/code/$OUTPUT_BASE/$AFTER png=1

# export OSM data from each revision
GITHUB_SHA=$GITHUB_SHA cicd/osm/scripts/export.sh local_output_dir=$OUTPUT_BASE/$BEFORE revision=$BEFORE
GITHUB_SHA=$GITHUB_SHA cicd/osm/scripts/export.sh local_output_dir=$OUTPUT_BASE/$AFTER revision=$AFTER

# create a geojson file showing MBRs of all geometry differences between the two revisions
cicd/scripts/pull_or_build.sh repo=tomfumb image=bvnordic-osm-renderer:2 build_dir=cicd/osm/docker/renderer context_dir=cicd upload_if_missing=$UPLOAD_IF_MISSING
docker run --rm -e REVISION=$BEFORE -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 ogr2ogr -f "GPKG" /code/$OUTPUT_BASE/compare.gpkg /workdir/main-data.gpkg -nln before -sql "SELECT * FROM Trails"
docker run --rm -e REVISION=$AFTER -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 ogr2ogr -f "GPKG" /code/$OUTPUT_BASE/compare.gpkg /workdir/main-data.gpkg -nln after -update -sql "SELECT * FROM Trails"
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 ogr2ogr -f "GeoJSON" /code/$OUTPUT_BASE/diff.geojson /code/$OUTPUT_BASE/compare.gpkg -nln diff -t_srs "EPSG:4326" -dialect sqlite -sql "SELECT geom FROM (SELECT ST_Envelope(ST_Difference(a.geom, b.geom)) AS geom FROM after a LEFT JOIN before b ON a.fid = b.fid UNION SELECT ST_Envelope(ST_Difference(b.geom, a.geom)) as geom FROM before b LEFT JOIN after a ON b.fid = a.fid) WHERE geom iS NOT NULL"
rm $OUTPUT_BASE/compare.gpkg

# render OSM data from each revision and merge to background imagery to provide context
docker run --rm -e REVISION=$BEFORE -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 /workdir/cicd/osm/docker/renderer/render.sh data_dir=/code/$OUTPUT_BASE/$BEFORE/main
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdalwarp -ts 1600 0 /code/cicd/imagery/output/network.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.tif
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdal_translate -of PNG -co zlevel=9 /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.tif /code/$OUTPUT_BASE/$BEFORE/main/bvnordic.osm-segments-merged.png
docker run --rm -e REVISION=$AFTER  -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 /workdir/cicd/osm/docker/renderer/render.sh data_dir=/code/$OUTPUT_BASE/$AFTER/main
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdalwarp -ts 1600 0 /code/cicd/imagery/output/network.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.tif
docker run --rm -v $PWD:/code tomfumb/bvnordic-osm-renderer:2 gdal_translate -of PNG -co zlevel=9 /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.tif /code/$OUTPUT_BASE/$AFTER/main/bvnordic.osm-segments-merged.png

# run change detection on before/after images
python -m cicd.compare.detect_changes $BEFORE $AFTER $PWD/$OUTPUT_BASE

# clean up 
rm -rf $OUTPUT_BASE/$BEFORE
rm -rf $OUTPUT_BASE/$AFTER

# upload results to Google Drive if necessary
if [ "$UPLOAD" == "1" ]; then
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO python -m cicd.upload.upload $COMPARE_DIR $PWD/output
fi