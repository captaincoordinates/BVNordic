#!/bin/bash

UNIQUE_REF="${GITHUB_SHA:-$(uuidgen)}"
export UNIQUE_DIR=$(date -u '+%Y%m%d')-$UNIQUE_REF
export LOCAL_OUTPUT_DIR=output/build/$UNIQUE_DIR
export CONTAINER_OUTPUT_DIR=/export/$LOCAL_OUTPUT_DIR