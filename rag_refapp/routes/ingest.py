from fastapi import APIRouter

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/")
async def ingest_document():
    return {"hello": "world"}
