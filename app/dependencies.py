from functools import lru_cache

from app.config import Settings
from app.opensearch.database import OpenSearchClient
from app.opensearch.database_config import OpenSearchConfig

"""
    This module serves as a singleton. This is Pythonic...?
"""


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_opensearch_config() -> OpenSearchConfig:
    return OpenSearchConfig(get_settings())


@lru_cache
def get_opensearch_client() -> OpenSearchClient:
    return OpenSearchClient(get_opensearch_config())
