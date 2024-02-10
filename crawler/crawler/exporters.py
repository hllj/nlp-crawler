from elasticsearch import Elasticsearch
from scrapy.utils.project import get_project_settings
from scrapy.exporters import BaseItemExporter


class ESItemExporter(BaseItemExporter):
    doc_type = 'Post'

    def __init__(self, **kwargs):
        super(ESItemExporter, self).__init__(**kwargs)
        settings = get_project_settings()
        self.elastic_hosts = settings.get('ELASTIC_HOSTS')
        self.index = settings.get('ELASTIC_INDEX')

        if self.elastic_hosts is not None:
            self.client = Elasticsearch(hosts=self.elastic_hosts)

    def start_exporting(self):
        pass

    def finish_exporting(self):
        pass

    def export_item(self, item):
        if self.client is None:
            return item
    
        item_id = item['item_id']
        self.client.index(
            index=self.index,
            id=item_id,
            document=dict(item)
        )
        return item