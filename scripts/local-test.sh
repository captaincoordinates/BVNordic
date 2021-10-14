#!/bin/bash

. scripts/directory.sh
mkdir -p $LOCAL_DIR
OUTPUT_BASE=$CONTAINER_DIR scripts/generate.sh