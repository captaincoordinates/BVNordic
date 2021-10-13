FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
  gnupg \
  software-properties-common \
  wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 46B5721DBBD2996A
RUN wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"

RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
  ca-certificates \
  python-qgis \
  qgis-server \
  xauth \
  xvfb \
  && rm -rf /var/lib/apt/lists/*

# assumes bind mount from ci directory to /export
CMD ["/export/ci/run.sh"]