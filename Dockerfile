FROM --platform=linux/amd64 ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Manila

# https://docs.gauge.org/howto/ci_cd/docker.html?os=null&language=python&ide=vscode

# Install dependencies - java, python, etc.
RUN apt-get clean && apt-get update && apt-get install -q -y \
    curl \
    zip \
    unzip \
    apt-transport-https \
    gnupg2 \
    ca-certificates \
    libaio1 \
    wget \
    openjdk-8-jdk \
    python3.9 \
    python-is-python3 \
    python3-pip \
    docker*

# Install Oracle Instant Client
WORKDIR /opt/oracle
# https://stackoverflow.com/questions/59269016/docker-python-use-odpi-c-for-oracle-db-connection#answer-59309143
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

WORKDIR /workspace/gauge-product-registry

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install colorama && \
    pip3 install -r requirements.txt

# Install gauge and plugins
RUN curl -SsL https://downloads.gauge.org/stable | sh && \
    gauge -v && \
    gauge install java && \
    gauge install python && \
    gauge install screenshot && \
    gauge install html-report

ENV PATH=$HOME/.gauge:$PATH