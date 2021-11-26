FROM ubuntu:21.10

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get install -y \
    libmapnik3.1 \
    mapnik-utils \
    osm2pgsql \
    osmium-tool \
    python3 \
    python3-mapnik \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get install -y \
    git \
    npm \
    nodejs \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g carto

RUN apt-get -y update \
    && apt-get install -y \
    fonts-noto-cjk \
    fonts-noto-hinted \
    fonts-noto-unhinted \
    fonts-hanazono \
    ttf-unifont \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get install -y \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get install -y \
    netcat \
    && rm -rf /var/lib/apt/lists/*

COPY docker/renderer/render.sh /render.sh
COPY docker/renderer/generate_image.py /generate_image.py

USER postgres
WORKDIR /source
RUN git clone --depth 1 https://github.com/gravitystorm/openstreetmap-carto.git

CMD [ "/render.sh" ]