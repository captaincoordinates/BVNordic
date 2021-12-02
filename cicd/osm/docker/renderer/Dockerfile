FROM ubuntu:21.10

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get install -y \
    curl \
    gdal-bin \
    jq \
    libmapnik3.1 \
    mapnik-utils \
    netcat \
    osm2pgsql \
    osmium-tool \
    postgresql-13-postgis-3 \
    python3 \
    python3-mapnik \
    python3-pip \
    python3-psycopg2 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g carto

USER postgres
WORKDIR /home/postgres