FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
  gnupg \
  software-properties-common \
  wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 46B5721DBBD2996A \
  && wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import \
  && chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg \
  && add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main" \
  && apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
  git \
  python-qgis \
  qgis-server \
  xauth \
  xvfb \
  && rm -rf /var/lib/apt/lists/*

COPY scripts/revision_entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]