import os
import sys

from dotenv import load_dotenv

if os.environ.get('BOT_TOKEN', None) is None:
    load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN', 'DO_NOT_PASTE_TOKEN_HERE')
DEBUG = False
IS_SERVERLESS = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# RESULTS_LIMIT is used both to limit results, returned by ES, and to limit InlineQueryResultPhoto entries
# However this doesn't affects search results ranking, because maximum search results limit in ES is 10000
# https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html
# Maximum limit for InlineQueryResultPhoto by Telegram API (@pic?) is 50
# RESULTS_LIMIT should be int
RESULTS_LIMIT = 50

LOCAL_FOLDER = os.path.join(os.sep, 'var', 'www', 'memeusbot')
STATIC_PROTO = "https://"
STATIC_DOMAIN = "memeus.sychusha.com"
STATIC_BASE_URL = "/static/"
STATIC_LOCAL_FOLDER = os.path.join(LOCAL_FOLDER, 'www')
DEFAULT_IMAGE_FILENAME = "image"
THUMBNAILS_HEIGHT = 200
THUMBNAIL_PREFIX = "thumb_"

ES_HOST = "localhost"
ES_PORT = 9200
ES_INDEX_NAME = "memeus"
ES_DOC_TYPE = "_doc"

# workaround for bot ModuleNotFoundError: No module named ...
sys.path.insert(0, BASE_DIR)


def construct_url(prefix, file_name):
    return STATIC_PROTO + STATIC_DOMAIN + STATIC_BASE_URL + prefix + '/' + file_name
