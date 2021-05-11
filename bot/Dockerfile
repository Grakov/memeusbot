FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python-is-python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
VOLUME /var/www/memeusbot
RUN useradd -m memeusbot
USER memeusbot

COPY . $HOME/memeusbot
COPY ../requirements.txt $HOME/requirements.txt
COPY ../www $HOME/www

WORKDIR $HOME
RUN pip3 install wheel && \
    pip3 install -r requirements.txt

WORKDIR $HOME/memeusbot

ENTRYPOINT ['python', 'bot.py']