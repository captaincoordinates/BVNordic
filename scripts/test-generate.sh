#!/bin/bash

set -e

pushd $(dirname $0)/..

GITHUB_SHA="test-$(uuidgen)" . scripts/directory.sh
mkdir -p $LOCAL_OUTPUT_DIR
OUTPUT_BASE=$LOCAL_OUTPUT_DIR scripts/generate.sh
LOCAL_OUTPUT_DIR=$LOCAL_OUTPUT_DIR scripts/osm.sh

if [ "$UPLOAD" == "1" ]; then
    UPLOAD_FOLDER_NAME=$UNIQUE_DIR scripts/upload.sh 
fi