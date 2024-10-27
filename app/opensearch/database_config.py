from app.config import Settings


class OpenSearchConfig:

    def __init__(self, settings: Settings):
        self.hostname: str = settings.opensearch_hostname
        self.port: int = settings.opensearch_port
        self.auth: dict[str, str] = {
            "username": settings.opensearch_username,
            "password": settings.opensearch_password,
        }
        self.ssl_flag: bool = settings.opensearch_ssl_flag
