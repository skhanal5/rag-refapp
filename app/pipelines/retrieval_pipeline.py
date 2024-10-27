from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.generators import HuggingFaceLocalGenerator
from haystack.utils import Secret
from haystack_integrations.components.retrievers.opensearch import (
    OpenSearchEmbeddingRetriever,
)
from haystack_integrations.document_stores.opensearch import (
    OpenSearchDocumentStore,
)

from app.config import Settings
from app.opensearch.database_config import OpenSearchConfig


class RetrievalPipeline:
    """
    Defines a pipeline that uses RAG functionality to generate
    a response to a query.
    """

    __system_prompt: str = """
        Given the following information, answer the question.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer:
        """

    def __init__(self, opensearch_config: OpenSearchConfig, settings: Settings):
        self.pipeline = Pipeline()
        self._opensearch_config = opensearch_config
        self._settings = settings

    def execute_pipeline(self, query: str):
        prompt_builder = PromptBuilder(template=RetrievalPipeline.__system_prompt)
        generator = HuggingFaceLocalGenerator(
            model=self._settings.text_generation_model,
            token=Secret.from_token(self._settings.hugging_face_token),
        )
        generator.warm_up()

        # Add all components for this pipeline
        self.pipeline.add_component(
            "text_embedder",
            SentenceTransformersTextEmbedder(
                model=self._settings.embedding_model,
                token=Secret.from_token(self._settings.hugging_face_token),
            ),  # Uses default model
        )
        self.pipeline.add_component(
            "retriever",
            OpenSearchEmbeddingRetriever(document_store=self.get_document_store()),
        )
        self.pipeline.add_component("prompt_builder", prompt_builder)
        self.pipeline.add_component("llm", generator)

        # Connect the components together
        self.pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "llm")

        # Execute the pipeline
        return self.pipeline.run(
            {
                "text_embedder": {"text": query},
                "prompt_builder": {"question": query},
            }
        )

    def get_document_store(self) -> OpenSearchDocumentStore:
        document_store = OpenSearchDocumentStore(
            hosts=self._opensearch_config.hostname,
            use_ssl=self._opensearch_config.ssl_flag,
            http_auth=self._opensearch_config.auth,
        )
        return document_store
