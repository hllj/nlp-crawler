# Vietnamese NLP Scrapy

Codebase để crawl data từ các trang web lớn của Việt Nam

# To Do

Các trang báo:

- [x] Thanhnien
- [ ] vnexpress

Các trang forum:

- [ ] VnZ
- [ ] Otofun
- [ ] Kenhsinhvien

# Cài đặt

## Các library cần thiết

```bash
pip install -r requirements.txt
```

## Các Database, Log

- [x] ElasticSearch + Kibana
- [ ] MongoDB

Cài đặt Docker + Docker-Compose. Chú ý chỉnh sửa dòng sau để thêm volume từ docker.
```yaml
volumes:
    - ./esdata:/home/lap15363/elasticsearch/data
```
Để start service ElasticSearch + Kibana
```bash
docker-compose up -d
```

Chờ khoảng 1 phút để network start. Các service sẽ port sau:

- ElasticSearch: localhost:9200
- Kibana: localhost:5601

# Setup spider và các setting

## Spider: 

Spiders sẽ chứa implement cách chúng ta crawl các trang.

Có thể sử dụng các loại SitemapSpider để parse các link từ sitemap nếu có. Có thể xem thử ví dụ từ crawler/spiders/thanhnien.py

Các loại spider khác có thể tham khảo [tại đây](https://docs.scrapy.org/en/latest/topics/spiders.html)

Có thể tham khảo ví dụ custom spider để tạo ra các requests, xem thử crawler/spiders/tv4u.py

## Items:

Items sẽ định nghĩa ra Schema của các item mỗi khi chúng ta crawl. 

Tham khảo các Item được implement trong crawler/items.py

## Exporters:

Exporters là nơi chúng ta implement cách export các item. 

Ở đây chúng ta có thể viết các cách để connect database và export item và import vào trong DB.

## Middlewares

Middlewares là trung gian giữa spiders và site, ở đây chúng ta có thể thêm một số middleware như:

- Random User-Agents: ngẫu nhiên chọn user-agent để gửi request tới site.
- Proxy Middlewares: ngẫu nhiên chọn các proxy để  gửi tới request site.
- Retry Middleware: cách để retry sau khi không kết nối tới được.

Có thể tham khảo thêm các lib sau sử dụng thay thế cho các middlewares:

- [Random User-Agents](https://github.com/cnu/scrapy-random-useragent)
- [Scrapy Rotating Proxies](https://github.com/TeamHG-Memex/scrapy-rotating-proxies)

## Pipelines

Định nghĩa các pipeline: luồng xử lý các item sau khi crawl được sẽ làm gì tiếp. Ở đây có thể chúng ta sẽ kết hợp các Exporters và Items để tạo ra Pipelines.

Tham khảo ESPipeline trong crawler/pipelines.py

## Settings

Trong file Settings.py sẽ là nơi chúng ta configure tất cả mọi thành phần ở trên.

Một số các configure quan trọng:

```bash
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# MAXIMUM TIME FOR A REQUEST
DOWNLOAD_TIMEOUT = 10

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False
```

```bash
# Number of retry times if a request failed
RETRY_TIMES = 10
```

Sử dụng các Middlewares: đưa ra thứ tự các con số cho các middlewares, None là tắt sử dụng middlewares đó.

```bash
DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.CrawlerAgentMiddleware": 100,
    # 'rotating_free_proxies.middlewares.RotatingProxyMiddleware': 200,
    # 'rotating_free_proxies.middlewares.BanDetectionMiddleware': 300,
    # "crawler.middlewares.CrawlerProxyMiddleware": 200,
    # "crawler.middlewares.CrawlerRetryMiddleware": 300,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
```

Sử dụng các Pipelines:

```bash
ITEM_PIPELINES = {
   "crawler.pipelines.CrawlerPipeline": 100,
   "crawler.pipelines.ESPipeline": 200,
}
```

Logging:

```bash
LOG_LEVEL = 'INFO'  # DEBUG for debug mode, ERROR for only display errors
LOG_FORMAT = '%(levelname)s: %(message)s'
LOG_FILE = 'crawl.log' # Logging filename
```

ElasticSearch Config (sử dụng trong ESExporters):
```bash
ELASTIC_HOSTS = [
    {'host': 'localhost', 'port': 9200, "scheme": "http"},
]
```

# Scrapy

Để bắt đầu crawl ta dùng lệnh sau:

```bash
cd crawler/crawler
```

```bash
scrapy crawl <spider name> --set JOBDIR=<job name>
```

Ex:

```bash
scrapy crawl thanhnien --set JOBDIR=thanhnien
```

Để tạm dừng và resume lại crawl, ta có thể nhấn Ctrl + C (chỉ một lần) và start lại lệnh trên. Scrapy sẽ tự động lưu một thư mục JOBDIR để start lại những URL chưa được chạy.