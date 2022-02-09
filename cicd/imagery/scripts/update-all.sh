#!/bin/bash

pushd $(dirname $0)/../../..

cicd/imagery/scripts/update-stadium.sh
