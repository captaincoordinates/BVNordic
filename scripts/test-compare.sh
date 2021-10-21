#!/bin/bash

set -e

pushd $(dirname $0)/..

docker build -t exporter layout
OUTPUT_BASE=output/compare-$1-$2
mkdir -p $OUTPUT_BASE/$1
mkdir -p $OUTPUT_BASE/$2
docker run --rm -v $PWD:/export -e OUTPUT_BASE=/export/$OUTPUT_BASE/$1 exporter /export/layout/generate.sh $1
docker run --rm -v $PWD:/export -e OUTPUT_BASE=/export/$OUTPUT_BASE/$2 exporter /export/layout/generate.sh $2