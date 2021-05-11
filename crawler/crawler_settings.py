import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# workaround for crawler ModuleNotFoundError: No module named ...
sys.path.insert(0, BASE_DIR)

LOCAL_FOLDER = os.path.join(os.sep, 'var', 'www', 'memeusbot')
STATIC_LOCAL_FOLDER = os.path.join(LOCAL_FOLDER, 'www')
DEFAULT_IMAGE_FILENAME = "image"
THUMBNAILS_HEIGHT = 200
THUMBNAIL_PREFIX = "thumb_"

ES_HOST = "localhost"
ES_PORT = 9200
ES_INDEX_NAME = "memeus"
ES_DOC_TYPE = "_doc"

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
                "fielddata": True,
            },
            "alt_tags": {
                "type": "text",
                "fielddata": True,
            },
            "description": {
                "type": "text",
                "fielddata": True,
            },
            "meaning": {
                "type": "text",
                "fielddata": True,
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
