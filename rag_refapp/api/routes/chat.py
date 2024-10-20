from fastapi import APIRouter
from pydantic import BaseModel

from rag_refapp.pipelines.retrieval_pipeline import RetrievalPipeline

router = APIRouter(prefix="/chat", tags=["index"])


class ChatDetails(BaseModel):
    query: str


@router.post("/")
async def add_index(request_body: ChatDetails):
    pipeline: RetrievalPipeline = RetrievalPipeline()
    pipeline.execute_pipeline(request_body.query)
