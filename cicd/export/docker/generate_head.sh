#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            png)         PNG=${VALUE} ;;
            pdf)         PDF=${VALUE} ;;
            output_base) OUTPUT_BASE=${VALUE} ;;
            *)   
    esac    
done

FORMATS=""
if [ -z ${PNG+x} ]; then
    FORMATS="$FORMATS --png"
fi
if [ -z ${PDF+x} ]; then
    FORMATS="$FORMATS --pdf"
fi

xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate main $OUTPUT_BASE $FORMATS
xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate stadium $OUTPUT_BASE $FORMATS