from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import Settings
from app.dependencies import get_opensearch_config, get_settings
from app.opensearch.database_config import OpenSearchConfig
from app.pipelines.markdown_pipeline import MarkdownPipeline

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestDetails(BaseModel):
    path: str


@router.post("/")
async def ingest_path(
    request_body: IngestDetails,
    opensearch_config: Annotated[OpenSearchConfig, Depends(get_opensearch_config)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    pipeline: MarkdownPipeline = MarkdownPipeline(opensearch_config, settings)
    return pipeline.execute_pipeline(request_body.path)
