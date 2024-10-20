from fastapi import APIRouter
from pydantic import BaseModel

from rag_refapp.pipelines.ingestion_pipeline import IngestionPipeline

router = APIRouter(prefix="/ingest", tags=["index"])


class IngestDetails(BaseModel):
    path: str


@router.post("/")
async def add_index(request_body: IngestDetails):
    pipeline: IngestionPipeline = IngestionPipeline()
    pipeline.execute_pipeline(request_body.path)
