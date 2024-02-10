import scrapy
from scrapy.spiders import SitemapSpider
from crawler.items import VNZItem

from bs4 import BeautifulSoup

import logging
import hashlib

class CrawlerSpider(SitemapSpider):
    name = "vnz"
    allowed_domains = ['vn-z.vn']
    sitemap_urls = ['https://vn-z.vn/sitemap.xml']
    sitemap_rules = [
        ('https://vn-z.vn/threads/*', 'parse'),
    ]
    
    source = 'vn-z.vn'
    
    def get_datetime(self, response):
        datetime = response.xpath("//time[@class='u-dt']/@datetime").extract_first()
        if datetime is not None:
            datetime = datetime.strip()
        return datetime
    
    def get_title(self, response):
        title = response.xpath('//h1[@class="title header-title"]/text()').extract_first()
        if title is None:
            title = response.xpath('//h1[@class="p-title-value"]/text()').extract_first()
        if title is not None:
            title = title.strip()
        return title
    
    def get_post(self, response):
        post = response.xpath('//div[@class="bbWrapper"]').extract_first()
        if post is not None:
            post = post.strip()
        return post
    
    def get_replies(self, response):
        replies = response.xpath('//div[@class="bbWrapper"]').extract()
        replies = replies[1:]
        return replies
        
    def parse(self, response, get_post=True):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        
        item = VNZItem()
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        id = m.hexdigest()
        
        item['item_id'] = id
        item['url'] = url
        item['source'] = self.source
        item['datetime'] = self.get_datetime(response)
        item['title'] = self.get_title(response)
        if get_post:
            item['post'] = self.get_post(response)
        else:
            item['post'] = ""
        item['replies'] = self.get_replies(response)
        
        logging.log(logging.INFO, f"crawl done {url}")
        
        yield item
        
        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=dict(get_post=False))