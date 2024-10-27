from pathlib import Path

from haystack import Pipeline
from haystack.components.converters import (
    MarkdownToDocument,
)
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret
from haystack_integrations.document_stores.opensearch import (
    OpenSearchDocumentStore,
)

from app.config import Settings
from app.opensearch.database_config import OpenSearchConfig


class MarkdownPipeline:
    """
    Defines a pipeline to ingest markdown files from
    your local filesystem
    """

    def __init__(
        self, opensearch_config: OpenSearchConfig, settings: Settings
    ):
        self.pipeline = Pipeline()
        self._opensearch_config = opensearch_config
        self._settings = settings

    def execute_pipeline(self, path: str):

        # TODO: works on markdown only
        files = list(Path(path).glob("*.md"))

        # Init dependencies for components
        document_writer = self._setup_writer()

        # Add all components for this
        self.pipeline.add_component(
            instance=MarkdownToDocument(), name="text_file_converter"
        )
        self.pipeline.add_component(instance=DocumentCleaner(), name="cleaner")
        self.pipeline.add_component(
            instance=DocumentSplitter(split_by="sentence", split_length=1),
            name="splitter",
        )
        self.pipeline.add_component(
            "text_embedder",
            SentenceTransformersDocumentEmbedder(
                model=self._settings.embedding_model,
                token=Secret.from_token(self._settings.hugging_face_token),
            ),  # Uses default model
        )
        self.pipeline.add_component(instance=document_writer, name="writer")

        # Connect the components together
        self.pipeline.connect(
            "text_file_converter.documents", "cleaner.documents"
        )
        self.pipeline.connect("cleaner.documents", "splitter.documents")
        self.pipeline.connect("splitter.documents", "text_embedder.documents")
        self.pipeline.connect("text_embedder.documents", "writer.documents")

        # Execute the pipeline
        return self.pipeline.run({"text_file_converter": {"sources": files}})

    def _setup_writer(self) -> DocumentWriter:
        document_store = OpenSearchDocumentStore(
            hosts=self._opensearch_config.hostname,
            use_ssl=self._opensearch_config.ssl_flag,
            http_auth=self._opensearch_config.auth,
        )
        document_writer = DocumentWriter(document_store=document_store)
        return document_writer
