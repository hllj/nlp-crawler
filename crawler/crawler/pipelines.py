# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from crawler.exporters import ESItemExporter
from bs4 import BeautifulSoup

import logging


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item

class ESPipeline(object):
    exporter = None

    def open_spider(self, spider):
        self.exporter = ESItemExporter()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        logging.log(logging.INFO, f"import to ES done {item['url']}")
        return item
