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
+--- scrapy.cfg             # Scrapy cfg-file
+--- www                    # HTTP root
|   +--- index.html
|   +--- static             # Downloaded images directory
```