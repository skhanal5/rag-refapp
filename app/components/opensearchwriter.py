# from haystack import component
#
# from app.opensearch.database import OpenSearchClient
# from app.opensearch.database_config import OpenSearchConfig
#
#
# @component
# class OpenSearchWriter:
#
#     def __init__(self, config: OpenSearchConfig):
#         self.client = OpenSearchClient(config)
#
#     @component.output_types()
#     def run(self):
#         # Should handle fetching from OpenSearch
#         # using our custom
#         pass
