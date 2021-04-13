from scrapy.item import Item, Field


class MemeArticle(Item):
    url = Field()
    tags = Field()
    alt_tags = Field()
    description = Field()
    meaning = Field()
    images = Field()
