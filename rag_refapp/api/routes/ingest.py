from fastapi import APIRouter
from pydantic import BaseModel

from rag_refapp.pipelines.ingestion_pipeline import IngestionPipeline

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestDetails(BaseModel):
    path: str


@router.post("/")
async def ingest_path(request_body: IngestDetails):
    pipeline: IngestionPipeline = IngestionPipeline()
    return pipeline.execute_pipeline(request_body.path)
