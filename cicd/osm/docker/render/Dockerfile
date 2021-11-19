FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get install -y \
    bzip2 \
    postgresql-13 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /source
RUN wget https://github.com/mapnik/mapnik/releases/download/v3.1.0/mapnik-v3.1.0.tar.bz2 \
    && bunzip2 mapnik-v3.1.0.tar.bz2 \
    && tar -xf mapnik-v3.1.0.tar \
    && rm mapnik-v3.1.0.tar*
WORKDIR /source/mapnik-v3.1.0

RUN apt-get -y update \
    && apt-get install -y \
    build-essential \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get install -y \
    curl \
    libfreetype6-dev \
    zlib1g \
    libicu-dev \
    libharfbuzz-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libboost-iostreams-dev \
    libboost-thread-dev \
    libboost-python-dev \
    libboost-program-options-dev \
    libboost-regex-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ./configure && JOBS=8 make && make test

RUN apt-get -y update \
    && apt-get install -y \
    osm2pgsql \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g carto
