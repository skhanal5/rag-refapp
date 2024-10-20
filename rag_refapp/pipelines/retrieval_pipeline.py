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


class RetrievalPipeline:

    pipeline: Pipeline

    def __init__(self):
        self.pipeline = Pipeline()

    def execute_pipeline(self, query: str):
        template = """
        Given the following information, answer the question.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer:
        """

        document_store = OpenSearchDocumentStore(
            hosts="http://localhost:9200",
            use_ssl=True,
            verify_certs=False,
            http_auth=("admin", "admin"),
        )

        prompt_builder = PromptBuilder(template=template)
        generator = HuggingFaceLocalGenerator(
            token=Secret.from_token("<your-api-key>")
        )
        generator.warm_up()

        # Add all components for this pipeline
        self.pipeline.add_component(
            "text_embedder", SentenceTransformersTextEmbedder(model="model")
        )
        self.pipeline.add_component(
            "retriever",
            OpenSearchEmbeddingRetriever(document_store=document_store),
        )
        self.pipeline.add_component("prompt_builder", prompt_builder)
        self.pipeline.add_component("llm", generator)

        # Connect the components together
        self.pipeline.connect(
            "text_embedder.embedding", "retriever.query_embedding"
        )
        self.pipeline.connect("retriever", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "llm")

        # Execute the pipeline
        self.pipeline.run(
            {"prompt_builder": {"query": query}, "retriever": {"query": query}}
        )
