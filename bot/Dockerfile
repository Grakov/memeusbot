FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python-is-python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install wheel && \
    pip3 install -r /tmp/requirements.txt

VOLUME /var/www/memeusbot
RUN useradd -m memeusbot
USER memeusbot
ENV HOME="/home/memeusbot"

COPY . $HOME/memeusbot
WORKDIR $HOME/memeusbot

RUN pip3 install wheel && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python", "main.py"]