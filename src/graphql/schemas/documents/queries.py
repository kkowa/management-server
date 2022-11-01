from __future__ import annotations

from asgiref.sync import sync_to_async
from strawberry.types import Info
from strawberry_django_plus.gql import relay

from src.apps.documents import models

from . import types


@relay.connection
async def folders(info: Info) -> list[types.Folder]:
    """List of user's folders."""
    user = info.context.request.scope["user"]

    return await sync_to_async(list)(models.Folder.objects.filter(owner=user))  # type: ignore[no-any-return]


@relay.connection
async def documents(info: Info) -> list[types.Document]:
    """List of documents in folders owned by user."""
    user = info.context.request.scope["user"]

    return await sync_to_async(list)(  # type: ignore[no-any-return]
        models.Document.objects.filter(folder__owner=user),
    )
