from opensearch.database_config import DatabaseConfig
from opensearchpy import OpenSearch


class VectorDatabase:

    client: OpenSearch

    def __init__(self, config: DatabaseConfig):
        self.client = OpenSearch(
            hosts=[{"host": config.hostname, "port": config.port}],
            http_auth=config.auth,
            use_ssl=config.ssl_flag,
            verify_certs=config.verify_cert_flag,
        )

    def create_index(self):
        pass

    def add_document(self):
        pass

    def search_document(self):
        pass

    def delete_document(self):
        pass

    def delete_index(self):
        pass
