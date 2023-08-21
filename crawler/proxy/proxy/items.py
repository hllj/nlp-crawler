# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    ip_address = scrapy.Field()
    port = scrapy.Field()
    code = scrapy.Field()
    country = scrapy.Field()
    anonymity = scrapy.Field()
    google = scrapy.Field()
    https = scrapy.Field()
    last_checked = scrapy.Field()
