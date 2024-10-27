from typing import Any

from opensearchpy import OpenSearch

from app.opensearch.database_config import OpenSearchConfig


# TODO: Look at API and determine if any return values are needed
# TODO: Propagate all exceptions back to user
class OpenSearchClient:
    def __init__(self, config: OpenSearchConfig):
        # Sync client
        self.client = OpenSearch(
            hosts=[{"host": config.hostname, "port": config.port}],
            http_auth=config.auth,
            use_ssl=config.ssl_flag,
        )

    def create_index(self, index_name: str) -> Any:
        body = {
            "settings": {"index": {"knn": True}},
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "passage_chunk_embedding": {
                        "type": "nested",
                        "properties": {"knn": {"type": "knn_vector", "dimension": 768}},
                    },
                }
            },
        }
        return self.client.indices.create(index_name, body)

    def add_document(self, index_name: str, document: dict[str, str]) -> Any:
        return self.client.index(index=index_name, body=document)

    def search_document(self, index_id: str, query: str) -> Any:
        database_query = {
            "size": 5,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "director"],
                }
            },
        }

        return self.client.search(
            body=database_query,
            index=index_id,
        )

    def delete_document(self, index_name: str, doc_id: str) -> Any:
        return self.client.delete(
            index=index_name,
            id=doc_id,
        )

    def delete_index(self, index_name: str) -> Any:
        return self.client.indices.delete(index=index_name)
