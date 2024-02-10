import scrapy
from scrapy.spiders import SitemapSpider
from crawler.items import ForumItem

from bs4 import BeautifulSoup
import os
import logging
import hashlib

remove_patterns = [
    '\t\t\t<script class="js-extraPhrases" type="application/json">\n'
    '\t\t\t{\n'
    '\t\t\t\t"lightbox_close": "Close",\n'
    '\t\t\t\t"lightbox_next": "Next",\n'
    '\t\t\t\t"lightbox_previous": "Previous",\n'
    '\t\t\t\t"lightbox_error": "The requested content cannot be loaded. '
    'Please try again later.",\n'
    '\t\t\t\t"lightbox_start_slideshow": "Start slideshow",\n'
    '\t\t\t\t"lightbox_stop_slideshow": "Stop slideshow",\n'
    '\t\t\t\t"lightbox_full_screen": "Full screen",\n'
    '\t\t\t\t"lightbox_thumbnails": "Thumbnails",\n'
    '\t\t\t\t"lightbox_download": "Download",\n'
    '\t\t\t\t"lightbox_share": "Share",\n'
    '\t\t\t\t"lightbox_zoom": "Zoom",\n'
    '\t\t\t\t"lightbox_new_window": "New window",\n'
    '\t\t\t\t"lightbox_toggle_sidebar": "Toggle sidebar"\n'
    '\t\t\t}\n'
    '\t\t\t</script>\n',
    
    '\t\t\t{\n'
    '\t\t\t\t"lightbox_close": "Close",\n'
    '\t\t\t\t"lightbox_next": "Next",\n'
    '\t\t\t\t"lightbox_previous": "Previous",\n'
    '\t\t\t\t"lightbox_error": "The requested content cannot be '
    'loaded. Please try again later.",\n'
    '\t\t\t\t"lightbox_start_slideshow": "Start slideshow",\n'
    '\t\t\t\t"lightbox_stop_slideshow": "Stop slideshow",\n'
    '\t\t\t\t"lightbox_full_screen": "Full screen",\n'
    '\t\t\t\t"lightbox_thumbnails": "Thumbnails",\n'
    '\t\t\t\t"lightbox_download": "Download",\n'
    '\t\t\t\t"lightbox_share": "Share",\n'
    '\t\t\t\t"lightbox_zoom": "Zoom",\n'
    '\t\t\t\t"lightbox_new_window": "New window",\n'
    '\t\t\t\t"lightbox_toggle_sidebar": "Toggle sidebar"\n'
    '\t\t\t}\n'
]

class CrawlerSpider(SitemapSpider):
    name = "hocmai"
    allowed_domains = ['diendan.hocmai.vn']
    sitemap_urls = ['https://diendan.hocmai.vn/sitemap.php']
    sitemap_rules = [
        ('https://diendan.hocmai.vn/threads/*', 'parse'),
    ]
    
    source = 'diendan.hocmai.vn'
    
    def get_meta(self, response):
        breadcrumb = response.xpath('//li[@itemprop="itemListElement"]//a//span/text()').extract()
        
        category_page_name = breadcrumb[1]
        category_name = breadcrumb[2]
    
        if category_page_name is not None:
            category_page_name = category_page_name.strip()
        
        if category_name is not None:
            category_name = category_name.strip()
            
        datetime = response.xpath('//time[@class="u-dt"]/text()').extract_first()
        if datetime is not None:
            datetime = datetime.strip()
        source = self.source
        return source, category_page_name, category_name, datetime
    
    def get_title(self, response):
        title = response.xpath('//h1[@class="p-title-value"]/text()').extract_first()
        if title is not None:
            title = title.strip()
        return title
    
    def clean_patterns(self, s):
        for p in remove_patterns:
            s = s.replace(p, '')
        return s
    
    def get_replies(self, response):
        replies = response.xpath('//div[@class="bbWrapper"]').extract()
        replies = [self.clean_patterns(reply) for reply in replies]
        return replies
    
    def parse_page(self, response):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        source, category_page_name, category_name, datetime = self.get_meta(response)
        
        title = self.get_title(response)
        post = []
        replies = self.get_replies(response)
        
        item = ForumItem()
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
        item['post'] = post
        item['replies'] = replies
        
        logging.log(logging.INFO, f"crawl done {url}")
        
        yield item
        
        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_page)
        
    def parse(self, response):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        source, category_page_name, category_name, datetime = self.get_meta(response)
        
        title = self.get_title(response)
        replies = self.get_replies(response)
        
        post = replies[0]
        replies = replies[1:]
        
        item = ForumItem()
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
        item['post'] = post
        item['replies'] = replies
        
        logging.log(logging.INFO, f"crawl done {url}")
        
        yield item
        
        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_page)