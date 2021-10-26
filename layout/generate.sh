#!/bin/bash

set -e

pushd $(dirname $0)/..

COMMAND="python3 layout/generate.py"

if [ -z ${1+x} ]; then
    # no commit hash provided
    COMMAND="$COMMAND --png --pdf"
else
    # commit hash provided
    tar -cf /snapshot.tar /export
    mkdir /snapshot
    tar -xf /snapshot.tar -C /snapshot
    pushd /snapshot/export
    git reset --hard HEAD
    git checkout .
    git -c advice.detachedHead=false checkout $1
    COMMAND="$COMMAND --png"
fi

PROJECT=main xvfb-run -s '+extension GLX -screen 0 1920x1080x24' $COMMAND
PROJECT=stadium xvfb-run -s '+extension GLX -screen 0 1920x1080x24' $COMMAND