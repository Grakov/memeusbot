from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch, FunctionScore


class MemeSearch:
    def __init__(self, es_instance: Elasticsearch, index_name: str, query_text: str, max_results=10):
        self.es = es_instance
        self.index_name = index_name
        self.query_text = query_text

        self.es_query = MultiMatch(
            query=query_text,
            fields=['tags^3', 'alt_tags^3', 'description^2', 'meaning^1'],
            tie_breaker=0.3,
        )

        self.es_search = Search().index(self.index_name).using(client=self.es)[0:max_results].query(self.es_query)
        self.response = None

    def execute(self):
        self.response = self.es_search.execute()
        if self.response.success():
            return [hit for hit in self.response]
        else:
            return []

    def es_response(self):
        return self.response

    def hits_count(self):
        return self.response.hits.total

    def is_empty(self):
        return self.response is None or self.hits_count() == 0
