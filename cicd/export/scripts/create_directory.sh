#!/bin/bash

export UNIQUE_DIR=$GITHUB_SHA
export LOCAL_OUTPUT_DIR=output/$UNIQUE_DIR
mkdir -p $LOCAL_OUTPUT_DIR