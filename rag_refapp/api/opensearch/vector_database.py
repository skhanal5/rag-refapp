from .database_config import DatabaseConfig
from opensearchpy import OpenSearch


# TODO: Look at API and determine if any return values are needed
class VectorDatabase:

    client: OpenSearch

    def __init__(self, config: DatabaseConfig):
        # Sync client
        self.client = OpenSearch(
            hosts=[{"host": config.hostname, "port": config.port}],
            http_auth=config.auth,
            use_ssl=config.ssl_flag,
            verify_certs=config.verify_cert_flag,
        )

    def create_index(self, index_name: str) -> any:
        body = {
            "settings": {"index": {"knn": True}},
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "passage_chunk_embedding": {
                        "type": "nested",
                        "properties": {
                            "knn": {"type": "knn_vector", "dimension": 768}
                        },
                    },
                }
            },
        }
        return self.client.indices.create(index_name, body)

    def add_document(self, index_name: str, document: str) -> any:
        return self.client.index(index=index_name, body=document)

    def search_document(self, index_id: str, query: str) -> any:
        query = {
            "size": 5,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "director"],
                }
            },
        }

        return self.client.search(
            body=query,
            index=index_id,
        )

    def delete_document(self, index_name: str, doc_id: str) -> any:
        return self.client.delete(
            index=index_name,
            id=doc_id,
        )

    def delete_index(self, index_name: str):
        return self.client.indices.delete(index=index_name)
