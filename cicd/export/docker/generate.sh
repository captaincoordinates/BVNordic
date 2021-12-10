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
if [ "$PNG" == "1" ]; then
    FORMATS="$FORMATS --png"
fi
if [ "$PDF" == "1" ]; then
    FORMATS="$FORMATS --pdf"
fi

pushd /workdir

xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate main $OUTPUT_BASE $FORMATS
xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate stadium $OUTPUT_BASE $FORMATS