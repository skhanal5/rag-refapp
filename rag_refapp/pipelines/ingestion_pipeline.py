from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.opensearch import (
    OpenSearchDocumentStore,
)


class EmbeddingPipeline:

    def __init__(self):
        self.pipeline = Pipeline()

    def execute_pipeline(self, documents: list[Document]):

        # Init dependencies for components
        document_writer = EmbeddingPipeline.__setup_writer()

        # Add all components for this pipeline
        self.pipeline.add_component(
            "text_embedder", SentenceTransformersTextEmbedder(model="model")
        )
        self.pipeline.add_component(instance=document_writer, name="writer")

        # Connect the components together
        self.pipeline.connect("text_embedder", "writer")

        # Execute the pipeline
        self.pipeline.run({"embedder": {"documents": documents}})

    @staticmethod
    def __setup_writer():
        document_store = OpenSearchDocumentStore(
            hosts="http://localhost:9200",
            use_ssl=True,
            verify_certs=False,
            http_auth=("admin", "admin"),
        )
        document_writer = DocumentWriter(document_store=document_store)
        return document_writer
