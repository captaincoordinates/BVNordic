#!/bin/bash

UUID=$(uuidgen)
UNIQUE_REF="${GITHUB_SHA:-$(uuidgen)}"
EXPORT_REF=$(date -u '+%Y%m%d')-$UNIQUE_REF
export EXPORT_DIR=output/build/$EXPORT_REF

cd $(dirname $0)/..
mkdir -p $EXPORT_DIR