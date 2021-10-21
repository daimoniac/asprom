FROM ubuntu:xenial
ENV DEBIAN_FRONTEND=noninteractive
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
ADD https://bootstrap.pypa.io/pip/2.7/get-pip.py /get-pip.py
RUN chmod +x /tini
RUN apt-get update && \
    apt-get -y install cron python2.7 nmap python-mysqldb python-nmap patch && \
    rm -rf /var/lib/apt/lists/*
RUN python2 /get-pip.py 
RUN pip2 install python-crontab==2.6.0 netaddr==0.8.0 paste==3.5.0 bottle==0.12.19 config==0.4.2 croniter==1.0.15
WORKDIR /asprom
COPY . .
# fix old style class in python-crontab leading to exception
RUN patch -p0 /usr/local/lib/python2.7/dist-packages/crontab.py < docker/patch-crontab.py
EXPOSE 8080
ENTRYPOINT ["/tini", "--"]
CMD ["docker/start.sh"]

