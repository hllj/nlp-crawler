import scrapy
from scrapy.spiders import SitemapSpider
from crawler.items import CrawlerItem

from bs4 import BeautifulSoup

import logging
import hashlib

class CrawlerSpider(SitemapSpider):
    name = "thanhnien"
    allowed_domains = ['thanhnien.vn']
    sitemap_urls = ['https://thanhnien.vn/sitemap.xml']
    sitemap_rules = [
        ('https://thanhnien.vn/*', 'parse'),
    ]
    
    source = 'thanhnien.vn'
    
    def get_meta(self, response):
        category_page_name = response.xpath('//a[@class="category-page__name"]/text()').extract_first()
        if category_page_name is not None:
            category_page_name = category_page_name.strip()
            
        category_name = response.xpath('//a[@data-role="cate-name"]/text()').extract_first()
        if category_name is not None:
            category_name = category_name.strip()
            
        datetime = response.xpath('//div[@data-role="publishdate"]/text()').extract_first()
        if datetime is not None:
            datetime = datetime.strip()
        source = self.source
        return source, category_page_name, category_name, datetime
    
    def get_title(self, response):
        title = response.xpath('//*[@data-role="title"]/text()').extract_first()
        if title is not None:
            title = title.strip()
        return title
    
    def get_sapo(self, response):
        sapo = response.xpath('//h2[@class="detail-sapo"]/text()').extract()
        return sapo
    
    def get_content(self, response):
        content = response.xpath('//div[@class="detail-cmain"]//p/text()').extract()
        return content
        
    def parse(self, response):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        source, category_page_name, category_name, datetime = self.get_meta(response)
        
        title = self.get_title(response)
        sapo =  self.get_sapo(response)
        content = self.get_content(response)
        
        item = CrawlerItem()
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        id = m.hexdigest()
        
        item['item_id'] = id
        item['url'] = url
        item['source'] = source
        item['category_page_name'] = category_page_name
        item['category_name'] = category_name
        item['datetime'] = datetime
        item['title'] = title
        item['sapo'] = sapo
        item['content'] = content
        
        logging.log(logging.INFO, f"crawl done {url}")
        
        yield item