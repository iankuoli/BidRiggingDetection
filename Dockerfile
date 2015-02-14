FROM ubuntu:14.04
MAINTAINER Wush Wu <wush978@gmail.com>

RUN \
    echo "deb http://tw.archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb-src http://tw.archive.ubuntu.com/ubuntu/ trusty multiverse" >> /etc/apt/sources.list && \
    echo "deb http://tw.archive.ubuntu.com/ubuntu/ trusty-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://tw.archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://tw.archive.ubuntu.com/ubuntu/ trusty-proposed main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://tw.archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    apt-get update

RUN \
    apt-get install -y --no-recommends node npm python-dev python-pip python-numpy python-scipy && \
    pip install networkx flask

EXPOSE 80
