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
COPY . $HOME/crawler
RUN mv $HOME/crawler/scrapy.cfg $HOME/scrapy.cfg
RUN mv $HOME/crawler/wait-for-it.sh $HOME/wait-for-it.sh
RUN chown -R memeusbot:memeusbot $HOME/crawler

USER memeusbot
WORKDIR $HOME

ENTRYPOINT ["scrapy", "crawl", "memepedia"]