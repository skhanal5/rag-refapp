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

    __system_prompt: str = """
        Given the following information, answer the question.

        Context:
        {% for document in documents %}
            {{ document.content }}
        {% endfor %}

        Question: {{question}}
        Answer:
        """

    def __init__(self):
        self.pipeline = Pipeline()

    def execute_pipeline(self, query: str):

        document_store = OpenSearchDocumentStore(
            hosts="http://localhost:9200",
            use_ssl=True,
            verify_certs=False,
            http_auth=("admin", "@ThisIsMyPassword123"),
        )

        prompt_builder = PromptBuilder(
            template=RetrievalPipeline.__system_prompt
        )
        generator = HuggingFaceLocalGenerator(
            token=Secret.from_token("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")
        )
        generator.warm_up()

        # Add all components for this pipeline
        self.pipeline.add_component(
            "text_embedder",
            SentenceTransformersTextEmbedder(
                token=Secret.from_token(
                    "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"
                )
            ),  # Uses default model
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
        return self.pipeline.run(
            {
                "text_embedder": {"text": query},
                "prompt_builder": {"question": query},
            }
        )
