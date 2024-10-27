from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_opensearch_client
from app.opensearch.database import OpenSearchClient

router = APIRouter(prefix="/index", tags=["index"])


class SetupDetails(BaseModel):
    index_name: str


class DocumentDetails(BaseModel):
    doc_id: str


class Document(BaseModel):
    contents: str


@router.post("/")
async def add_index(
    request_body: SetupDetails,
    client: Annotated[OpenSearchClient, Depends(get_opensearch_client)],
):
    return client.create_index(request_body.index_name)


@router.delete("/")
async def delete_index(
    request_body: SetupDetails,
    client: Annotated[OpenSearchClient, Depends(get_opensearch_client)],
):
    return client.delete_index(request_body.index_name)


@router.post("/{index_name}/document")
async def add_document(
    index_name: str,
    request_body: Document,
    client: Annotated[OpenSearchClient, Depends(get_opensearch_client)],
):
    return client.add_document(index_name, {"contents": request_body.contents})


@router.delete("/{index_name}/document")
async def delete_document(
    index_name: str,
    request_body: DocumentDetails,
    client: Annotated[OpenSearchClient, Depends(get_opensearch_client)],
):
    return client.delete_document(index_name, request_body.doc_id)
