#!/bin/bash

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            before) BEFORE=${VALUE} ;;
            after)  AFTER=${VALUE} ;;     
            *)   
    esac    
done

export COMPARE_DIR=compare-$BEFORE-$AFTER
export OUTPUT_BASE=output/$COMPARE_DIR
mkdir -p $OUTPUT_BASE/$BEFORE
mkdir -p $OUTPUT_BASE/$AFTER