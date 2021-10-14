#!/bin/bash

echo "### OUTPUT_BASE $OUTPUT_BASE"
echo "### Current"
pwd

docker build -t exporter output
docker run --rm -v $PWD:/export -e OUTPUT_BASE exporter /export/output/export.sh