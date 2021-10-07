#!/bin/sh

cd `dirname $0`/..

xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 ci/export.py