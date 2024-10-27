from app.config import Settings


class OpenSearchConfig:

    def __init__(self, settings: Settings):
        self.hostname = settings.opensearch_hostname
        self.port = settings.opensearch_port
        self.auth = {
            "username": settings.opensearch_username,
            "password": settings.opensearch_password,
        }
        self.ssl_flag = settings.opensearch_ssl_flag
