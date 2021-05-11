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

RUN useradd -m memeusbot
RUN mkdir -p /var/www/memeusbot ; chown -R memeusbot:memeusbot /var/www/memeusbot
VOLUME /var/www/memeusbot

ENV HOME="/home/memeusbot"
COPY . $HOME/memeusbot
RUN chown -R memeusbot:memeusbot $HOME/memeusbot

USER memeusbot
WORKDIR $HOME/memeusbot

ENTRYPOINT ["python", "main.py"]