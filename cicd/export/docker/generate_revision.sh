#!/bin/bash

set -e

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            png)         PNG=${VALUE} ;;
            pdf)         PDF=${VALUE} ;;     
            revision)    REVISION=${VALUE} ;;
            output_base) OUTPUT_BASE=${VALUE} ;;
            *)   
    esac    
done

if [ -z ${REVISION+x} ]; then
    echo "'revision' parameter mandatory"
    exit 1
fi

FORMATS=""
if [ "$PNG" == "1" ]; then
    FORMATS="$FORMATS --png"
fi
if [ "$PDF" == "1" ]; then
    FORMATS="$FORMATS --pdf"
fi

mkdir /snapshot
cp -R /code /snapshot/
pushd /snapshot/code
git reset --hard HEAD
git checkout .
git -c advice.detachedHead=false checkout $REVISION
rm -rf cicd
cp -R /code/cicd .

xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate main $OUTPUT_BASE $FORMATS
xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 -m cicd.export.generate stadium $OUTPUT_BASE $FORMATS