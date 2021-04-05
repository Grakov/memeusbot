import scrapy
import json

from crawler.items import MemeArticle
from crawler.spider_db import *

# selectors
MEMEPEDIA_BASIC_SELECTOR = 'article div.single-main-container div.col-content div.s-post-content img'
MEMEPEDIA_CATEGORY_SELECTOR = 'article nav ol li.ordinal-item span'
MEMEPEDIA_PREVIEW_SELECTOR = 'article div.single-main-container div.col-content figure.post-thumbnail img'
MEMEPEDIA_TITLE_SELECTOR = 'title'
MEMEPEDIA_HEADLINE_SELECTOR = 'article div.single-main-container div.col-content header.s-post-header h1'
MEMEPEDIA_GALLERY_SELECTOR = 'div.bb-post-gallery-content ul.bb-gl-slide li figure.bb-gl-image img'

MEMEPEDIA_EXCLUDES = [
    'https://memepedia.ru/wp-content/uploads/2021/01/tg5.jpg'
]
MEMEPEDIA_URL_EXCLUDES = [
    'wp-login',
    'tel:'
]
MEMEPEDIA_SUITABLE_CATEGORIES = {
    'Мемы': 'meme',
    'Омагад': 'article'
}

MEMEPEDIA_ACCEPTED_CONTENT_TYPES = ["text/html", "application/xhtml+xml", "application/xml",
                                    "text/webviewhtml", "text/x-server-parsed-html"]


class MemeSpider(scrapy.Spider):
    name = 'memepedia'
    allowed_domains = [
        'memepedia.ru'
    ]
    start_urls = [
        'https://memepedia.ru/memoteka/',
        'https://memepedia.ru/category/memes/',
        'https://memepedia.ru/category/omagad/'
    ]

    def parse(self, response):
        tags = set()
        pictures = set()
        category = None
        if not response.headers['content-type'].decode("utf-8").split(';')[0].lower() in MEMEPEDIA_ACCEPTED_CONTENT_TYPES:
            return

        # get type of material
        for breadcrumb in response.css(MEMEPEDIA_CATEGORY_SELECTOR):
            breadcrumb_text = breadcrumb.css('::text').get().strip()
            if breadcrumb_text in MEMEPEDIA_SUITABLE_CATEGORIES:
                category = MEMEPEDIA_SUITABLE_CATEGORIES.get(breadcrumb_text, None)

        if category is not None:
            # get title and headline
            title = response.css(MEMEPEDIA_TITLE_SELECTOR).css('::text').get().strip()
            headline = response.css(MEMEPEDIA_HEADLINE_SELECTOR).css('::text').get().strip()
            if title != '':
                tags.add(title)
            if headline != '':
                tags.add(headline)

            # add preview picture
            preview_image = response.css(MEMEPEDIA_PREVIEW_SELECTOR)
            if len(preview_image) > 0:
                p_src = preview_image[0].attrib.get('src', None)
                if p_src is not None:
                    pictures.add(p_src)

            # parse pictures
            # @TODO change list to set for tags (like on pictures)
            for item in response.css(MEMEPEDIA_BASIC_SELECTOR):
                src = item.attrib.get('src', None)
                tag = item.attrib.get('alt', None)

                if src is None or src in MEMEPEDIA_EXCLUDES:
                    continue
                pictures.add(src)

                if tag is not None:
                    tags.add(tag)

            # parse galleries
            for item in response.css(MEMEPEDIA_GALLERY_SELECTOR):
                src = item.attrib.get('src', None)
                if src is not None:
                    pictures.add(src.strip())

            if len(tags) > 0:
                yield MemeArticle(url=response.url, images=list(pictures), tags=list(tags))

        # save data to DB
        if not check_indexed_url(response.url, IndexedPagesTable):
            page_row = IndexedPagesTable(url=response.url, tags=json.dumps(list(tags)), media=json.dumps(list(pictures)))
            db_session.add(page_row)
            db_session.commit()

        # @TODO add exception for urls with '/page/'
        for next_page in response.css('a'):
            url = next_page.attrib.get('href', None)
            if url is not None:
                if (not check_indexed_url(url, IndexedPagesTable) and self.is_allowed_url(url)) or url in self.start_urls:
                    yield response.follow(url, self.parse)

    def is_allowed_url(self, url):
        for rule in MEMEPEDIA_URL_EXCLUDES:
            if url.find(rule) != -1:
                return False
        return True
