FROM debian:bookworm-slim
ENV TINI_VERSION=v0.19.0
ENV DEBIAN_FRONTEND=noninteractive
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
COPY requirements.txt /tmp/
RUN apt-get update && \
    apt-get -y install cron nmap patch libmariadb3 python3-minimal python3-pip \
      default-libmysqlclient-dev build-essential pkg-config && \
    pip install --break-system-packages -r /tmp/requirements.txt && \
    apt-get -y autoremove python3-dev python3-pip default-libmysqlclient-dev \
      build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /asprom
COPY . .
# fix old style class in python-crontab leading to exception
RUN patch -p0 /usr/local/lib/python3.11/dist-packages/crontab.py < docker/patch-crontab.py
RUN chmod 640 aspromNagiosCheck.py
EXPOSE 8080
ENTRYPOINT ["/tini", "--"]
CMD ["docker/start.sh"]

