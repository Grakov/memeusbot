# MemeusBot 

Telegram bot, which search memes in inline mode. Includes web crawler for [memepedia.ru](https://memepedia.ru) and bot itself.

Made with [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI), [Elasticsearch](https://www.elastic.co/) ([Python Elasticsearch Client](https://elasticsearch-py.readthedocs.io/) + [elasticsearch-dsl](https://elasticsearch-dsl.readthedocs.io/)) and flavored with [Scrapy](https://scrapy.org/).

## Installation
* [Download](https://www.elastic.co/downloads/elasticsearch) and [setup](https://www.elastic.co/downloads/elasticsearch#installation-steps) Elasticsearch (*7.X* branch).
* Create [virtual environment](https://docs.python.org/3/tutorial/venv.html).
* Install via ``pip`` packages listed in ``requirements.txt``.
* If you don't already have a Telegram bot, [create](https://core.telegram.org/bots#6-botfather) one and obtain authorization token.
* Paste your Telegram bot's token in ``bot/.env`` file: 

```
BOT_TOKEN="TOKEN:GOES_HERE"
```
Alternatively you can paste it in ``docker-compose.yaml`` in ``environment`` section for bot service (Docker only).

Bot and crawler (except Scrapy) settings are available in ``bot/settings.py`` and ``crawler/crawler_settings.py``.

Replace ``example.com`` with your domain:

```
STATIC_PROTO = "https://"
STATIC_DOMAIN = "example.com"
```

Elasticsearch connection settings are also available here:

```
ES_INDEX_NAME = "memeus"
ES_HOST = "localhost"
ES_PORT = 9200
ES_DOC_TYPE = "_doc"
```

You can also check Scrapy [configuration](https://docs.scrapy.org/en/latest/topics/settings.html) (rate-limits, etc) on ``crawler/settings.py`` or change DB connection settings on ``crawler/spider_bot.py`` (SQLAlchemy).

## Running crawler
Run this command to start ``crawler`` in the top directory of project:
```
scrapy crawl memepedia
```

## Starting bot
* On Linux
```
python bot/main.py
```
* On Windows
```
python bot\main.py
```

## Docker
You can use Dockerfiles from this project for running Memeusbot project in Docker.
Dockerfiles are available separately for all instances: bot, crawler and nginx for serving static files

Before running any container, you should create docker volume (in these examples named ``bot_storage``).
It will be mounted on every container to ``/var/www/memeusbot``:
```
docker volume create bot_storage
```

### Bot
Make Docker image via ``Dockerfile`` and run container based on it:
```
cd bot
docker image build -t memeusbot_bot -f Dockerfile . 
docker container run -d --name memeusbot_bot -v bot_storage:/var/www/memeusbot memeusbot_bot
```

### Crawler
Make Docker image via ``Dockerfile`` and run container based on it:
```
cd crawler
docker image build -t memeusbot_crawler -f Dockerfile . 
docker container run -d --name memeusbot_crawler -v bot_storage:/var/www/memeusbot memeusbot_crawler
```

### Nginx
Nginx is optional and needed only if you want to serve images from your server. 
By default it's configured to be used as ``proxy_pass`` backend. So nginx on your host is required.

Make Docker image via ``Dockerfile`` and run container based on it:
```
cd nginx
docker image build -t memeusbot_nginx -f Dockerfile . 
docker container run -d --name memeusbot_nginx -v bot_storage:/var/www/memeusbot -p 127.0.0.1:8080:80 memeusbot_nginx
```

## Known issues

Unfortunately on Telegram for Windows search results aren't displayed with bot setting ``IS_SERVERLESS = False``.

## Project structure
```
+--- bot                    # bot directory
|   +--- .env
|   +--- main.py            # Main bot script
|   +--- search.py          # Searching in memeus ES index
|   +--- settings.py        # Bot's settings
+--- crawler                # Scrapy crawler directory
|   +--- crawler_settings.py # Crawler settings 
|   +--- importer.py        # Importing data to memeus ES index
|   +--- items.py 
|   +--- models.py          # DB tables models
|   +--- pipelines.py       # Saving scrapped data
|   +--- settings.py        # Scrapy settings
|   +--- spiders
|   |   +--- memepedia.py   # Spider for memepedia.ru
|   +--- spider_db.py       # DB config
+--- elasticsearch          # Dockerfile and configs for dockered Elasticsearch
+--- nginx                  # Dockerfile and configs for dockered nginx
+--- www                    # HTTP root
|   +--- index.html
|   +--- static             # Downloaded images directory
+--- docker-compose.yaml    # Docker-compose config file
+--- requirements.txt       # Python pip requirements
+--- scrapy.cfg             # Scrapy cfg-file
```