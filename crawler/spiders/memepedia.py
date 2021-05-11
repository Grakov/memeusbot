import scrapy
import json

from crawler.items import MemeArticle
from crawler.spider_db import *

# selectors
MEMEPEDIA_BASIC_SELECTOR = 'article div.single-main-container div.col-content div.s-post-content img'
MEMEPEDIA_CONTENT_SELECTOR = 'article div.single-main-container div.col-content div.s-post-content'
MEMEPEDIA_ALT_TAGS_SELECTOR = 'p b,p strong'
MEMEPEDIA_PARAGRAPH_SELECTOR = 'p, h2'
MEMEPEDIA_IMG_DESCRIPTIONS_SELECTOR = 'p em'
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
    '/users/',
    'tel:',
    'mailto:',
    'shop.memepedia.ru'
]
MEMEPEDIA_CACHE_EXCLUDES = [
    '/page/'
]
MEMEPEDIA_TAG_EXCLUDES = [
    'Ctrl+Enter'
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
        alt_tags = ''
        pictures = set()
        category = None
        description = ''
        meaning = list()

        if not response.headers['content-type'].decode("utf-8").split(';')[
                   0].lower() in MEMEPEDIA_ACCEPTED_CONTENT_TYPES:
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

            article_content = response.css(MEMEPEDIA_CONTENT_SELECTOR)

            # @TODO should I replace \xa0 with ' '?
            # get alt tags and description
            alt_tags_element = article_content.css(MEMEPEDIA_ALT_TAGS_SELECTOR)
            if len(alt_tags_element) > 0:
                alt_tags = ''.join(alt_tags_element[0].css('::text').getall()).strip()
                description = ''.join(article_content.css(MEMEPEDIA_PARAGRAPH_SELECTOR)[0].css('p::text').getall()).strip()

            # get meme meaning
            meaning_header_found = False
            for paragraph in article_content.css(MEMEPEDIA_PARAGRAPH_SELECTOR):
                header_check = paragraph.css('h2')

                if len(header_check) > 0:
                    if meaning_header_found:
                        break

                    if header_check.css('::text').get() is not None and \
                            header_check.css('::text').get().strip() == 'Значение':
                        meaning_header_found = True
                else:
                    if meaning_header_found:
                        meaning.append(''.join(paragraph.css('::text').getall()).strip())

            # parse pictures
            for item in response.css(MEMEPEDIA_BASIC_SELECTOR):
                src = item.attrib.get('src', None)
                tag = item.attrib.get('alt', None)

                if src is None or src == '' or src in MEMEPEDIA_EXCLUDES:
                    continue
                pictures.add(src)

                if tag is not None and len(tag) > 0 and tag not in MEMEPEDIA_TAG_EXCLUDES:
                    tags.add(tag)

            # parse notes for images
            for img_description in article_content.css(MEMEPEDIA_IMG_DESCRIPTIONS_SELECTOR):
                tag = img_description.css('::text').get()
                if tag is not None:
                    tag = tag.strip()
                    if len(tag) > 0 and tag not in MEMEPEDIA_TAG_EXCLUDES:
                        tags.add(tag)

            # parse galleries
            for item in response.css(MEMEPEDIA_GALLERY_SELECTOR):
                src = item.attrib.get('src', None)
                if src is not None:
                    pictures.add(src.strip())

            if len(tags) > 0:
                yield MemeArticle(url=response.url, images=list(pictures), tags=list(tags), alt_tags=alt_tags,
                                  description=description, meaning=meaning)

        # save data to DB
        if not is_url_indexed(response.url, IndexedPagesTable) and self.is_url_cacheable(response.url):
            page_row = IndexedPagesTable(url=response.url, tags=json.dumps(list(tags)), alt_tags=alt_tags,
                                         media=json.dumps(list(pictures)))
            db_session.add(page_row)
            db_session.commit()

        for next_page in response.css('a'):
            url = next_page.attrib.get('href', None)
            if url is not None:
                if (not is_url_indexed(url, IndexedPagesTable) and self.is_url_allowed(url)) or url in self.start_urls:
                    yield response.follow(url, self.parse)

    def is_url_allowed(self, url):
        for rule in MEMEPEDIA_URL_EXCLUDES:
            if url.find(rule) != -1:
                return False
        return True

    def is_url_cacheable(self, url):
        for rule in MEMEPEDIA_CACHE_EXCLUDES:
            if url.find(rule) != -1:
                return False

        if url in self.start_urls:
            return False

        return True
