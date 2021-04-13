from elasticsearch import Elasticsearch


class MemeImporter:
    def __init__(self, es_instance: Elasticsearch, index_name: str, doc_name: str):
        self.es = es_instance
        self.index_name = index_name
        self.doc_name = doc_name

    def insert(self, image_id: str, tags: list, alt_tags: str, description: str, meaning: list, file_name: str,
               article_url: str, original_url: str):
        self.es.index(index=self.index_name, doc_type=self.doc_name, id=image_id, body={
            "id": image_id,
            "tags": tags,
            "alt_tags": alt_tags,
            "description": description,
            "meaning": meaning,
            "file_name": file_name,
            "article_url": article_url,
            "original_url": original_url
        })
