FROM ubuntu:21.10

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update \
    && apt-get install -y \
    gdal-bin \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt