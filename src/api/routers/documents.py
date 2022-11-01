from typing import Any

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from src.apps.documents import datamodels, models

router = APIRouter(prefix="/documents", tags=["Documents"])


class Document(BaseModel):
    """Model schema for `Document` model."""

    id: str

    class Config:
        orm_mode = True


class CreateDocument(BaseModel):
    """Input schema for `create_documents` endpoint."""

    folder: str
    data: Any


@router.post(
    path="",
    summary="Create bulk of documents",
    status_code=status.HTTP_201_CREATED,
    response_model=list[Document],
)
async def create_documents(request: Request, documents: list[CreateDocument]) -> list[Document]:
    """Create new documents. Any non-existing folders will be created automatically."""
    owner = request.user

    return [
        Document.from_orm(document)
        for document in await sync_to_async(models.Document.objects.create_documents_with_folders)(
            owner=owner,
            input=[
                datamodels.CreateDocumentInput(
                    folder=document.folder,
                    data=document.data,
                )
                for document in documents
            ],
        )
    ]
