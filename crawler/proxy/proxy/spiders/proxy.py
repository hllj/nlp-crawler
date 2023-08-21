from scrapy import Spider
from scrapy.selector import Selector

from proxy.items import ProxyItem

class DmozSpider(Spider):
    name = "proxy"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = [
        "https://free-proxy-list.net/"
    ]

    def parse(self, response):
        rows = response.xpath('//table[@class="table table-striped table-bordered"]//tr')
        for tr in rows[1:-1]:
            columns = tr.xpath('.//td/text()').extract()
            if len(columns) == 8:
                item = ProxyItem()
                item['ip_address'] = columns[0]
                item['port'] = columns[1]
                item['code'] = columns[2]
                item['country'] = columns[3]
                item['anonymity'] = columns[4]
                item['google'] = columns[5]
                item['https'] = columns[6]
                item['last_checked'] = columns[7]
                yield item