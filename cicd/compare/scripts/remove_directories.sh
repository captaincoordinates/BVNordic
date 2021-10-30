#!/bin/bash

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            before)      BEFORE=${VALUE} ;;
            after)       AFTER=${VALUE} ;;
            output_base) OUTPUT_BASE=${VALUE} ;;
            *)   
    esac    
done

rm -rf $OUTPUT_BASE/$BEFORE
rm -rf $OUTPUT_BASE/$AFTER