from __future__ import annotations

from asgiref.sync import sync_to_async
from strawberry.scalars import JSON
from strawberry.types import Info
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

from src.apps.documents import datamodels, models

from . import types


@gql.input
class CreateDocumentInput:
    folder: str
    data: JSON  # type: ignore[valid-type]


@gql.type
class CreateDocumentsOutput:
    documents: list[types.Document]


@relay.input_mutation
async def create_documents(info: Info, documents: list[CreateDocumentInput]) -> CreateDocumentsOutput:
    """Create bulk of documents."""
    user = info.context.request.scope["user"]

    return CreateDocumentsOutput(  # type: ignore[call-arg]
        documents=await sync_to_async(models.Document.objects.create_documents_with_folders)(
            owner=user,
            input=[
                datamodels.CreateDocumentInput(
                    folder=document.folder,
                    data=document.data,
                )
                for document in documents
            ],
        )
    )
