from fastapi import APIRouter
from pydantic import BaseModel

from rag_refapp.api.opensearch.database_config import DatabaseConfig
from rag_refapp.api.opensearch.vector_database import VectorDatabase

router = APIRouter(prefix="/ingest", tags=["ingest"])
config = DatabaseConfig(
    hostname="localhost",
    port=9200,
    auth=("admin", "@ThisIsMyPassword123"),
    ssl_flag=True,
    verify_cert_flag=False,
    ssl_show_warn=False,
)
database = VectorDatabase(config)


class SetupDetails(BaseModel):
    index_name: str


@router.post("/setup/")
async def setup_index(request_body: SetupDetails):
    return database.create_index(request_body.index_name)
