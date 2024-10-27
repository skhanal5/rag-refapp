from app.config import Settings


class OpenSearchConfig:
    def __init__(self, settings: Settings):
        self.hostname: str = settings.opensearch_hostname
        self.port: int = settings.opensearch_port
        self.auth: (str, str) = (
            settings.opensearch_username,
            settings.opensearch_password,
        )
        self.ssl_flag: bool = settings.opensearch_ssl_flag
