#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            png)                PNG=${VALUE} ;;
            pdf)                PDF=${VALUE} ;;
            permit_label_locks) PERMIT_LABEL_LOCKS=${VALUE} ;;
            output_base)        OUTPUT_BASE=${VALUE} ;;
            *)   
    esac    
done

FORMATS_ARG=""
if [ "$PNG" == "1" ]; then
    FORMATS_ARG="$FORMATS --png"
fi
if [ "$PDF" == "1" ]; then
    FORMATS_ARG="$FORMATS --pdf"
fi
LABEL_LOCKS_ARG=""
if [ "$PERMIT_LABEL_LOCKS" == "1" ]; then
    LABEL_LOCKS_ARG="--permit_label_locks"
fi

pushd /workdir

xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate main $OUTPUT_BASE $FORMATS_ARG $LABEL_LOCKS_ARG
xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate stadium $OUTPUT_BASE $FORMATS_ARG $LABEL_LOCKS_ARG