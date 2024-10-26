from fastapi import APIRouter
from pydantic import BaseModel

from app.api.opensearch.database_config import DatabaseConfig
from app.api.opensearch.vector_database import VectorDatabase

router = APIRouter(prefix="/index", tags=["index"])
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


class DocumentDetails(BaseModel):
    doc_id: str


class Document(BaseModel):
    contents: str


@router.post("/")
async def add_index(request_body: SetupDetails):
    return database.create_index(request_body.index_name)


@router.delete("/")
async def delete_index(request_body: SetupDetails):
    return database.delete_index(request_body.index_name)


@router.post("/{index_name}/document")
async def add_document(index_name: str, request_body: Document):
    return database.add_document(
        index_name, {"contents": request_body.contents}
    )


@router.delete("/{index_name}/document")
async def delete_document(index_name: str, request_body: DocumentDetails):
    return database.delete_document(index_name, request_body.doc_id)
