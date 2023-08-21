# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    item_id = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    category_page_name = scrapy.Field()
    category_name=  scrapy.Field()
    datetime = scrapy.Field()
    title = scrapy.Field()
    sapo = scrapy.Field()
    content = scrapy.Field()