import scrapy
from scrapy.spiders import Spider
from crawler.items import ForumItem

from bs4 import BeautifulSoup
import os
import logging
import hashlib

remove_patterns = [
    '"lightbox_close": "Close",\n'
    '"lightbox_next": "Next",\n'
    '"lightbox_previous": "Previous",\n'
    '"lightbox_error": "The requested content cannot be loaded. Please '
    'try again later.",\n'
    '"lightbox_start_slideshow": "Start slideshow",\n'
    '"lightbox_stop_slideshow": "Stop slideshow",\n'
    '"lightbox_full_screen": "Full screen",\n'
    '"lightbox_thumbnails": "Thumbnails",\n'
    '"lightbox_download": "Download",\n'
    '"lightbox_share": "Share",\n'
    '"lightbox_zoom": "Zoom",\n'
    '"lightbox_new_window": "New window",\n'
    '"lightbox_toggle_sidebar": "Toggle sidebar"\n'
    '}\n',

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
    '\t\t\t\t"lightbox_toggle_sidebar": "Toggle sidebar"\n',

    '"lightbox_close": "Close",\n'
    '"lightbox_next": "Next",\n'
    '"lightbox_previous": "Previous",\n'
    '"lightbox_error": "The requested content cannot be loaded. Please '
    'try again later.",\n'
    '"lightbox_start_slideshow": "Start slideshow",\n'
    '"lightbox_stop_slideshow": "Stop slideshow",\n'
    '"lightbox_full_screen": "Full screen",\n'
    '"lightbox_thumbnails": "Thumbnails",\n'
    '"lightbox_download": "Download",\n'
    '"lightbox_share": "Share",\n'
    '"lightbox_zoom": "Zoom",\n'
    '"lightbox_new_window": "New window",\n'
    '"lightbox_toggle_sidebar": "Toggle sidebar"\n',
    
    '"lightbox_close": "Close",\n'
    '"lightbox_next": "Next",\n'
    '"lightbox_previous": "Previous",\n'
    '"lightbox_error": "The requested content cannot be loaded. Please '
    'try again later.",\n'
    '"lightbox_start_slideshow": "Start slideshow",\n'
    '"lightbox_stop_slideshow": "Stop slideshow",\n'
    '"lightbox_full_screen": "Full screen",\n'
    '"lightbox_thumbnails": "Thumbnails",\n'
    '"lightbox_download": "Download",\n'
    '"lightbox_share": "Share",\n'
    '"lightbox_zoom": "Zoom",\n'
    '"lightbox_new_window": "New window",\n'
    '"lightbox_toggle_sidebar": "Toggle sidebar"\n',
]

class CrawlerSpider(Spider):
    name = "kenhsinhvien"
    allowed_domains = ['kenhsinhvien.vn']
    sitemap_urls = ['https://kenhsinhvien.vn/sitemap.xml']
    sitemap_rules = [
        ('https://kenhsinhvien.vn/topic/*', 'parse'),
    ]
    
    source = 'kenhsinhvien.vn'
    
    # custom_settings = { 
    #   'ELASTIC_INDEX': 'kenhsinhvien', 
    # }
    
    sitemap_folder = './sitemap'
    
    def __init__(self, *args, **kwargs):
       self.ELASTIC_INDEX = kwargs.pop('ELASTIC_INDEX', None)
       super(CrawlerSpider).__init__(*args, **kwargs)
    
    def start_requests(self):
        
        for i in range(1, 10):
            sitemap_filename = os.path.join(self.sitemap_folder, f'sitemap-{i}.xml')
            with open(sitemap_filename, 'r') as f:
                file = f.read()
            soup = BeautifulSoup(file, 'xml')
            locs = soup.find_all('loc')
            for idx, loc in enumerate(locs):
                url = loc.text
                if 'topic' not in url:
                    continue
                # We need to check this has the http prefix or we get a Missing scheme error
                yield scrapy.Request(url=url, callback=self.parse)    
    
    
    def get_meta(self, response):
        category_page_name = None
        category_name = None
        breadcrumbs = response.xpath('//ul[@class="p-breadcrumbs "]//li//span/text()').extract()
        if len(breadcrumbs) > 0:
            category_page_name = breadcrumbs[0]
            if len(breadcrumbs) > 0:
                category_name = breadcrumbs[1]
        
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
    
    def get_replies(self, response):
        htmls = response.xpath('//div[@itemprop="text"]/div[@class="bbWrapper"]')
        replies = []
        for html in htmls:
            html = html.extract()
            soup = BeautifulSoup(html, "html.parser")
            reply = "".join(soup.strings)
            replies.append(reply)
        return replies
    
    def get_post(self, reponse):
        post = reponse.xpath('//div[@data-lb-universal="1"]//div[not(@itemprop)]/div[@class="bbWrapper"]').extract_first()
        if post is None:
            return ""
        soup = BeautifulSoup(post, "html.parser")
        post = "".join(soup.strings)
        return post
    
    def clean_patterns(self, s):
        for p in remove_patterns:
            s = s.replace(p, '')
        return s
        
    def parse(self, response):
        if response.request.meta.get('redirect_urls'):
            url = response.request.meta['redirect_urls'][0]
        else:
            url = response.request.url
        source, category_page_name, category_name, datetime = self.get_meta(response)
        
        title = self.get_title(response)
        post = self.clean_patterns(self.get_post(response))
        replies = [self.clean_patterns(reply) for reply in self.get_replies(response)]
        
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
        
        next_page = response.xpath("//a[@class='pageNavSimple-el pageNavSimple-el--next']/@href").extract_first()
        next_page = response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)