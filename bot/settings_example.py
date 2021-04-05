import os

BOT_TOKEN = "TOKEN:GOES_HERE"
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

RESULTS_LIMIT = None

STATIC_PROTO = "https://"
STATIC_DOMAIN = "example.com"
STATIC_BASE_URL = "/static/"
STATIC_LOCAL_FOLDER = os.path.join(BASE_DIR, 'www', 'static')
DEFAULT_IMAGE_FILENAME = "image"
THUMBNAILS_HEIGHT = 200
THUMBNAIL_PREFIX = "thumb_"

ES_HOST = "localhost"
ES_PORT = 9200
ES_INDEX_NAME = "memeus"
ES_DOC_TYPE = "_doc"

# TODO: read about installing dictionaries
# https://www.elastic.co/guide/en/elasticsearch/guide/current/hunspell.html
ES_INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "filter": {
                "ru_RU": {
                    "type": "hunspell",
                    "language": "ru_RU"
                }
            },
            "analyzer": {
                "ru_RU": {
                    "tokenizer":  "standard",
                    "filter":   ["lowercase", "ru_RU"]
                }
            },
            "blocks": {
                "read_only_allow_delete": "false"
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword",
            },
            "tags": {
                "type": "text",
            },
            "file_name": {
                "type": "keyword",
            },
            "article_url": {
                "type": "keyword",
            },
            "original_url": {
                "type": "keyword",
            },
        }
    }
}


def construct_url(prefix, file_name):
    return STATIC_PROTO + STATIC_DOMAIN + STATIC_BASE_URL + prefix + '/' + file_name
