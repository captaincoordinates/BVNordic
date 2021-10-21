#!/bin/bash

set -e

pushd $(dirname $0)/..

docker build -t exporter output
docker run --rm -v $PWD:/export -e OUTPUT_BASE=/export/$OUTPUT_BASE exporter /export/output/generate.sh