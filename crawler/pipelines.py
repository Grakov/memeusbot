from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

import shutil
import requests
import mimetypes
import os
import hashlib
import json
from PIL import Image

from crawler.spider_db import *
from crawler import crawler_settings as settings
from crawler.importer import MemeImporter

es = Elasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT}])

# check, if index exists
if not es.indices.exists(index=settings.ES_INDEX_NAME):
    es.indices.create(index=settings.ES_INDEX_NAME, body=settings.ES_INDEX_SETTINGS)


class MemePipeline(object):
    def process_item(self, item, spider):
        for image_url in item['images']:

            # check if we already downloaded image
            es_query = Search().index(settings.ES_INDEX_NAME).using(client=es).query("match", original_url=image_url)
            response = es_query.execute()

            # @TODO: add tags for existing images (by hash)
            if is_url_indexed(image_url, IndexedMediaTable) or response.success() and len(response.hits) != 0:
                continue

            # downloading file
            http_request = requests.get(image_url)
            if http_request.status_code == 200:
                sha256_hash = hashlib.sha256(http_request.content).hexdigest()

                # checking if www and www/static exists
                if not os.path.exists(settings.STATIC_LOCAL_FOLDER):
                    os.makedirs(settings.STATIC_LOCAL_FOLDER, exist_ok=True)

                index_html_path = os.path.join(settings.WWW_LOCAL_FOLDER, 'index.html')
                if not os.path.exists(index_html_path):
                    shutil.copyfile(os.path.join(settings.BASE_DIR, 'crawler', 'www', 'index.html'), index_html_path)

                # saving image
                file_ext = mimetypes.guess_extension(http_request.headers['content-type'])
                image_folder = os.path.join(settings.STATIC_LOCAL_FOLDER, sha256_hash)
                os.mkdir(image_folder)

                image_filename = settings.DEFAULT_IMAGE_FILENAME + file_ext
                image_full_path = os.path.join(image_folder, image_filename)

                with open(image_full_path, "wb") as output_image:
                    output_image.write(http_request.content)

                # generating thumbnail
                thumb = Image.open(image_full_path)
                thumb_size = ((thumb.width * settings.THUMBNAILS_HEIGHT / thumb.height), settings.THUMBNAILS_HEIGHT)
                thumb.thumbnail(thumb_size)
                thumb.save(os.path.join(image_folder, settings.THUMBNAIL_PREFIX + image_filename))

                # adding image to ES
                MemeImporter(es, index_name=settings.ES_INDEX_NAME, doc_name=settings.ES_DOC_TYPE).insert(
                    image_id=sha256_hash,
                    tags=item['tags'],
                    alt_tags=item['alt_tags'],
                    description=item['description'],
                    meaning=item['meaning'],
                    file_name=image_filename,
                    article_url=item['url'],
                    original_url=image_url
                )

                # save data to DB
                media_row = IndexedMediaTable(url=image_url, id=sha256_hash, hash=sha256_hash,
                                              file_name=image_filename, tags=json.dumps(item['tags']),
                                              alt_tags=item['alt_tags'], description=item['description'],
                                              meaning=json.dumps(item['meaning']), article_url=item['url'])
                db_session.add(media_row)
                db_session.commit()

        return item
