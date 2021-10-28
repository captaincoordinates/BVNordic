#!/bin/bash

pushd $(dirname $0)/..

echo "attempting to compare '$1' with '$2'"

git merge-base --is-ancestor 54775c7ad5850ca4b33b7f2f806095f2e04255f1 $1
SUPPORTS_COMPARISON=$?

git merge-base --is-ancestor $1 $2
CORRECT_ORDER=$?

if [ $SUPPORTS_COMPARISON -ne 0 ] ; then
    echo "$1 is too old to support comparison"
    exit 1
fi

if [ $CORRECT_ORDER -ne 0 ]; then
    echo "$1 is not an ancestor of $2, comparison not possible"
    exit 1
fi

docker build -t exporter layout
OUTPUT_BASE=output/compare-$1-$2
mkdir -p $OUTPUT_BASE/$1
mkdir -p $OUTPUT_BASE/$2
docker run --rm -v $PWD:/export -e OUTPUT_BASE=/export/$OUTPUT_BASE/$1 exporter /export/layout/generate.sh $1
docker run --rm -v $PWD:/export -e OUTPUT_BASE=/export/$OUTPUT_BASE/$2 exporter /export/layout/generate.sh $2
COMPARE_DIR=$PWD/$OUTPUT_BASE
pushd compare
python -m src.compare $1 $2 $COMPARE_DIR
popd
rm -rf $OUTPUT_BASE/$1
rm -rf $OUTPUT_BASE/$2

# upload.sh in current form may be layout-specific with --update_latest parameter. This concept is not relevant for comparisons
if [ "$UPLOAD" == "1" ]; then
    UPLOAD_ROOT=$PWD/output
    COMPARE_ROOT="compare-$1-$2"
    pushd upload
    GDRIVE_UPLOAD_SERVICE_ACCT_INFO=$GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO python -m src.upload $COMPARE_ROOT $UPLOAD_ROOT
    popd
fi