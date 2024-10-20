from pathlib import Path

from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret
from haystack_integrations.document_stores.opensearch import (
    OpenSearchDocumentStore,
)


class IngestionPipeline:

    def __init__(self):
        self.pipeline = Pipeline()

    def execute_pipeline(self, path: str):

        # TODO: works on markdown only
        files = list(Path(path).glob("*.md"))

        # Init dependencies for components
        document_writer = IngestionPipeline.__setup_writer()

        # Add all components for this
        self.pipeline.add_component(
            instance=TextFileToDocument(), name="text_file_converter"
        )
        self.pipeline.add_component(instance=DocumentCleaner(), name="cleaner")
        self.pipeline.add_component(
            instance=DocumentSplitter(split_by="sentence", split_length=1),
            name="splitter",
        )
        self.pipeline.add_component(
            "text_embedder",
            SentenceTransformersTextEmbedder(
                token=Secret.from_token("<your-api-key>")
            ),  # Uses default model
        )
        self.pipeline.add_component(instance=document_writer, name="writer")

        # Connect the components together
        self.pipeline.connect(
            "text_file_converter.documents", "cleaner.documents"
        )
        self.pipeline.connect("cleaner.documents", "splitter.documents")
        self.pipeline.connect("splitter.documents", "writer.documents")
        self.pipeline.connect("text_embedder", "writer")

        # Execute the pipeline
        self.pipeline.run({"embedder": {"documents": files}})

    @staticmethod
    def __setup_writer():
        document_store = OpenSearchDocumentStore(
            hosts="http://localhost:9200",
            use_ssl=True,
            verify_certs=False,
            http_auth=("admin", "@ThisIsMyPassword123"),
        )
        document_writer = DocumentWriter(document_store=document_store)
        return document_writer
