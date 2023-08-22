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

