#!/bin/bash

pushd $(dirname $0)/..


GITHUB_SHA=$(uuidgen) . scripts/directory.sh
mkdir -p $LOCAL_OUTPUT_DIR
OUTPUT_BASE=$CONTAINER_OUTPUT_DIR scripts/generate.sh
UPLOAD_FOLDER_NAME=$UNIQUE_DIR scripts/upload.sh
