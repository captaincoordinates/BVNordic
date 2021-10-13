#!/bin/bash

docker build -t exporter output
docker run --rm -v $PWD:/export -e OUTPUT_BASE exporter /export/output/export.sh