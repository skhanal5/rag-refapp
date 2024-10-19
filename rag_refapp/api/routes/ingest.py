from fastapi import APIRouter

from rag_refapp.api.opensearch.database_config import DatabaseConfig
from rag_refapp.api.opensearch.vector_database import VectorDatabase

router = APIRouter(prefix="/ingest", tags=["ingest"])
config = DatabaseConfig(
    hostname="0.0.0.0",
    port=9200,
    auth=("admin", "@ThisIsMyPassword123"),
    ssl_flag=False,
    verify_cert_flag=False,
    ssl_show_warn=False,
)
database = VectorDatabase(config)


@router.post("/")
async def setup_index(index_name: str):
    return database.create_index(index_name)


@router.post("/")
async def ingest_document(index_name: str):
    return database.add_document(index_name, "")
