# Vietnamese NLP Scrapy

Codebase to crawl data from major Vietnamese websites

# To Do

News websites:

- [x] [Thanhnien](https://drive.google.com/file/d/1EAuRpeeNec0NkRgU4qJZSGlRbJySbjCL/view?usp=drive_link)
- [ ] vnexpress

Forums:

- [x] [VnZ](https://drive.google.com/file/d/1ypp2caSRbIMAgES2esCLRm8MtCTfTu1l/view?usp=drive_link)
- [ ] Otofun
- [x] [Kenhsinhvien](https://drive.google.com/file/d/1Mve-jod12evo9JQOE8tLYmBwrn66EbYK/view?usp=drive_link)
- [x] [Hocmai](https://drive.google.com/file/d/1QJIQH5Vq9GNlx_0W8o3Ved-XLfcGY96c/view?usp=drive_link)

# Installation

## Libraries

```bash
pip install -r requirements.txt
```

## Tech Stack

- [x] ElasticSearch + Kibana
- [ ] MongoDB

Install Docker + Docker-Compose. Note: Edit the following line to add volume from docker.

```yaml
volumes:
    - ./esdata:/home/lap15363/elasticsearch/data
```

To start service with ElasticSearch + Kibana

```bash
docker-compose up -d
```

Wait about 1 minute for the network to start (default: localhost). Services will be ported as follows:

- ElasticSearch: 9200
- Kibana: 5601

# Setup spiders and Setting

## Spider: 

Spiders will contain an implementation of how we crawl pages.

You can use SitemapSpider types to parse links from the sitemap if available. You can see an example from crawler/spiders/thanhnien.py

Other types of spiders can be referenced [here](https://docs.scrapy.org/en/latest/topics/spiders.html)

You can refer to my custom spider example to make requests, check out crawler/spiders/tv4u.py

## Items:

Items will define the Schema of the items every time we crawl.

Refer to Items implemented in crawler/items.py

## Exporters:

Exporters is where we implement how to export items.

Here we can write ways to connect database and export items and import into DB.

## Middlewares

Middlewares are intermediaries between spiders and the site, here we can add some middleware such as:

- Random User-Agents: randomly select user-agents to send requests to the site.
- Proxy Middlewares: randomly select proxies to send to the request site.
- Retry Middleware: how to retry after failing to connect.

You can refer to the following libs to use instead of middlewares:

- [Random User-Agents](https://github.com/cnu/scrapy-random-useragent)
- [Scrapy Rotating Proxies](https://github.com/TeamHG-Memex/scrapy-rotating-proxies)

## Pipelines

Defining pipelines: the flow of processing items after crawling, what to do next. Here we may combine Exporters and Items to create Pipelines.

Refer to ESPipeline in crawler/pipelines.py

## Settings

In the Settings.py file will be where we configure all the above components.

Some important configurations:

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

Use Middlewares: give the order of numbers for middlewares, None is to turn off the use of that middlewares.

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

Pipelines:

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

To start crawling, we use:

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

To pause and resume crawling, we can press Ctrl + C (only once) and restart the above command. Scrapy will automatically save a JOBDIR folder to restart URLs that have not been run.