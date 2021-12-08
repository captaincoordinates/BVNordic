FROM osgeo/gdal:ubuntu-small-3.1.0

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get install -y \
    git \
    libxml2-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY osm/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY scripts/revision_entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
