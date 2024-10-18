from database.database_config import DatabaseConfig
from opensearchpy import OpenSearch


# TODO: Proper return values
class VectorDatabase:

    client: OpenSearch

    def __init__(self, config: DatabaseConfig):
        self.client = OpenSearch(
            hosts=[{"host": config.hostname, "port": config.port}],
            http_auth=config.auth,
            use_ssl=config.ssl_flag,
            verify_certs=config.verify_cert_flag,
        )

    def create_index(self, index_name: str) -> any:
        response = self.client.indices.create(index_name)
        return response

    def add_document(self, index_name: str, doc_id: str) -> any:
        response = self.client.index(index=index_name, id=doc_id)
        return response

    def search_document(self, body: str, index_id: str) -> any:
        response = self.client.search(
            body=body,
            index=index_id,
        )
        return response

    def delete_document(self, index_name: str, doc_id: str) -> any:
        response = self.client.delete(
            index=index_name,
            id=doc_id,
        )
        return response

    def delete_index(self, index_name: str):
        response = self.client.indices.delete(index=index_name)
        return response
