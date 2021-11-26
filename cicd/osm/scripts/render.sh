#!/bin/bash

pushd $(dirname $0)/../../..

docker-compose -f cicd/osm/docker/docker-compose.yml up -d

# docker-compose -f cicd/osm/docker/docker-compose.yml down