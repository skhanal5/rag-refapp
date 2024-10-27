from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import Settings
from app.dependencies import get_settings, get_opensearch_config
from app.opensearch.database_config import OpenSearchConfig
from app.pipelines.retrieval_pipeline import RetrievalPipeline

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatDetails(BaseModel):
    query: str


@router.post("/")  # type: ignore
async def add_index(
    request_body: ChatDetails,
    opensearch_config: Annotated[OpenSearchConfig, Depends(get_opensearch_config)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> Any:
    pipeline: RetrievalPipeline = RetrievalPipeline(opensearch_config, settings)
    return pipeline.execute_pipeline(request_body.query)
