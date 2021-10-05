FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends \
  xvfb \
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
#   apache2 \
#   libapache2-mod-fcgid \
#   postgresql-client \
#   python3-pip \
  python-qgis \
  qgis \
  && rm -rf /var/lib/apt/lists/*
# RUN a2enmod fcgid
# RUN mkdir -p /var/run/apache2

# RUN pip3 install psycopg2

# ENV \
    # Apache config
    # APACHE_CONFDIR=/etc/apache2 \
    # APACHE_RUN_USER=www-data \
    # APACHE_RUN_GROUP=www-data \
    # APACHE_RUN_DIR=/var/run/apache2 \
    # APACHE_PID_FILE=/var/run/apache2/apache2.pid \
    # APACHE_LOG_DIR=/var/log/apache2 \
    # FCGI config
    # MAX_REQUESTS_PER_PROCESS=1000 \
    # MIN_PROCESSES=1 \
    # MAX_PROCESSES=10 \
    # BUSY_TIMEOUT=180 \
    # IDLE_TIMEOUT=600 \
    # IO_TIMEOUT=90

# RUN mkdir -p /home/qgis/projects/
# RUN mkdir -p /home/qgis/qgisserverdb
# RUN mkdir -p /var/log/qgis/
# RUN chown www-data:www-data /var/log/qgis
# RUN chown www-data:www-data /home/qgis/qgisserverdb

# COPY config /config
# COPY qgis.demo.conf /etc/apache2/conf-enabled/

# COPY run.sh /usr/local/bin/run.sh
# RUN chmod +x /usr/local/bin/run.sh




# CMD ["/usr/local/bin/run.sh"]
CMD ["tail", "-f", "/dev/null"]