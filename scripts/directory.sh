#!/bin/bash

echo "GITHUB_SHA: "$GITHUB_SHA
echo "uuidgen: "$(uuidgen)
echo "substitution: ""${GITHUB_SHA:-$(uuidgen)}"
TMP="${GITHUB_SHA:-$(uuidgen)}"
echo "TMP: "$TMP
TMP2="_$TMP"
echo "TMP2: "$TMP2

export UNIQUE_DIR="${GITHUB_SHA:-$(uuidgen)}"
export LOCAL_OUTPUT_DIR=output/build/$UNIQUE_DIR
export CONTAINER_OUTPUT_DIR=/export/$LOCAL_OUTPUT_DIR