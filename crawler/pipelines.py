from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

import requests
import mimetypes
import os
import uuid
import hashlib
import json
from PIL import Image

from crawler.spider_db import *
from bot import settings as bot_settings

es = Elasticsearch([{'host': bot_settings.ES_HOST, 'port': bot_settings.ES_PORT}])

# check, if index exists
if not es.indices.exists(index=bot_settings.ES_INDEX_NAME):
    es.indices.create(index=bot_settings.ES_INDEX_NAME, body=bot_settings.ES_INDEX_SETTINGS)


class MemePipeline(object):
    def process_item(self, item, spider):
        for image_url in item['images']:

            # check if we already downloaded image
            es_query = Search().index(bot_settings.ES_INDEX_NAME).using(client=es).query("match", original_url=image_url)
            response = es_query.execute()

            if check_indexed_url(image_url, IndexedMediaTable) or response.success() and len(response.hits) != 0:
                continue

            # downloading file
            http_request = requests.get(image_url)
            if http_request.status_code == 200:
                file_ext = mimetypes.guess_extension(http_request.headers['content-type'])
                tmp_file_name = os.path.join(bot_settings.TMP_DIR, str(uuid.uuid4()) + file_ext)
                sha256_hash = hashlib.sha256(http_request.content).hexdigest()

                with open(tmp_file_name, "wb") as output_image:
                    output_image.write(http_request.content)

                image_folder = os.path.join(bot_settings.STATIC_LOCAL_FOLDER, sha256_hash)
                os.mkdir(image_folder)

                image_final_filename = bot_settings.DEFAULT_IMAGE_FILENAME + file_ext
                image_full_path = os.path.join(image_folder, image_final_filename)
                os.rename(tmp_file_name, image_full_path)

                # generating thumbnail
                thumb = Image.open(image_full_path)
                thumb_size = ((thumb.width * bot_settings.THUMBNAILS_HEIGHT / thumb.height), bot_settings.THUMBNAILS_HEIGHT)
                thumb.thumbnail(thumb_size)
                thumb.save(os.path.join(image_folder, bot_settings.THUMBNAIL_PREFIX + image_final_filename))

                # adding image to ES
                es.index(index=bot_settings.ES_INDEX_NAME, doc_type=bot_settings.ES_DOC_TYPE, id=sha256_hash, body={
                    "id": sha256_hash,
                    "tags": item['tags'],
                    "file_name": image_final_filename,
                    "article_url": item['url'],
                    "original_url": image_url
                })

                # save data to DB
                media_row = IndexedMediaTable(url=image_url, id=sha256_hash, hash=sha256_hash,
                                              file_name=image_final_filename, tags=json.dumps(item['tags']))
                db_session.add(media_row)
                db_session.commit()

        return item
