#!/bin/bash

set -e

cp -R /code /workdir
pushd /workdir

if [ -z ${REVISION+x} ]; then
    echo "'revision' env var not provided, executing on HEAD"
else
    echo "executing on revision '$REVISION'"
    git reset --hard HEAD
    git checkout .
    git -c advice.detachedHead=false checkout $REVISION
    rm -rf cicd
    cp -R /code/cicd .
fi

"$@"