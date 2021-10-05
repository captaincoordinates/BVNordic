#!/bin/sh

# Xvfb :1 -screen 0 1024x768x24 &
xvfb-run -s '+extension GLX -screen 0 1024x768x24'
export DISPLAY=:1.0

cd `dirname $0`/..

echo `pwd`

echo "export 1"
QGIS_DEBUG=9 qgis --nologo --project ./main.qgs --code ./ci/export.py

echo "export 2"
python3 ci/export2.py
