from scrapy.item import Item, Field


class MemeArticle(Item):
    url = Field()
    tags = Field()
    images = Field()
