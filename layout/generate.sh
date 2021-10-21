#!/bin/bash

cd $(dirname $0)/..

PROJECT=main xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 layout/generate.py
PROJECT=stadium xvfb-run -s '+extension GLX -screen 0 1920x1080x24' python3 layout/generate.py