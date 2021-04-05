from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class MemeSearch:
    def __init__(self, es_instance: Elasticsearch, index_name: str):
        self.es = es_instance
        self.index_name = index_name
        self.response = None
        self.es_query = None

    def query(self, query_text: str):
        self.reset()
        self.es_query = Search().index(self.index_name).using(client=self.es).query("match", tags=query_text)
        return self

    def execute(self):
        self.response = self.es_query.execute()
        if self.response.success():
            return [hit for hit in self.response]
        else:
            # @TODO: replace return with throw?
            return []

    def reset(self):
        self.response = None
        self.es_query = None

    def es_response(self):
        return self.response

    def hits_count(self):
        return self.response.hits.total

    def is_empty(self):
        return self.response is None or self.hits_count() == 0
