#!/bin/bash

UNIQUE_REF="${GITHUB_SHA:-$(uuidgen)}"
EXPORT_REF=$(date -u '+%Y%m%d')-$UNIQUE_REF
export LOCAL_OUTPUT_DIR=output/build/$EXPORT_REF
export CONTAINER_OUTPUT_DIR=/export/$LOCAL_OUTPUT_DIR