FROM ubuntu:xenial

WORKDIR /usr/local

RUN apt-get update; \
    apt-get install -y curl python python-matplotlib imagemagick; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "/usr/local/bin/dedup.py"]
