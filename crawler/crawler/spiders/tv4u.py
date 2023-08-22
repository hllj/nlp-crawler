import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from crawler.items import TV4UItem

from bs4 import BeautifulSoup

import logging

class CrawlerSpider(Spider):
    name = "tve-4u"
    allowed_domains = ['http://tve-4u.org', 'tve-4u.org']
    # sitemap_urls = ['http://tve-4u.org/sitemap.php']
    # sitemap_rules = [('threads', 'parse_threads')]
    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[@class='text' and text() = 'Tiếp >']",)), callback="parse_pages", follow= True),)
    
    def start_requests(self):
        # url = "https://tve-4u.org/threads/lappel-de-lange-guillaume-musso.3222/"
        # yield scrapy.Request(url=url, callback=self.parse_threads)
        with open('tv4.xml', 'r') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'xml')
        locs = soup.find_all('loc')
        for idx, loc in enumerate(locs):
            url = loc.text
            if 'threads' not in url:
                continue
            # We need to check this has the http prefix or we get a Missing scheme error
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url
            yield scrapy.Request(url=url, callback=self.parse_threads)
    
    def get_content_messages(self, response):
        messages = response.xpath("//div[@class='messageContent']//blockquote[@class='messageText SelectQuoteContainer ugc baseHtml']").getall()
        return messages
    
    def get_attachments(self, response):
        attachments = response.xpath("//li[@class='attachment']//div[@class='thumbnail']//a/@href").getall()
        return attachments
    
    def get_html(self, response):
        html = response.xpath("//div[@id='content']").extract()
        return html
    
    def parse_threads(self, response):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        messages = self.get_content_messages(response)
        attachments = self.get_attachments(response)
        html = self.get_html(response)
        
        item = TV4UItem()
        item['url'] = url
        item['messages'] = messages
        item['attachments'] = attachments
        item['html'] = html
        
        logging.log(logging.INFO, f"Crawl done {url}")
        
        yield item
        
        next_page = response.xpath("//a[@class='text' and text() = 'Tiếp >']/@href").extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_threads)
        