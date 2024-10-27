from functools import lru_cache

from app import config
from app.opensearch.database import OpenSearchClient
from app.opensearch.database_config import OpenSearchConfig

"""
    This module serves as a singleton. This is Pythonic...?
"""


@lru_cache
def get_settings():
    return config.Settings()


@lru_cache
def get_opensearch_config():
    return OpenSearchConfig(get_settings())


@lru_cache
def get_opensearch_client():
    return OpenSearchClient(get_opensearch_config())
