from __future__ import annotations

import asyncio
from itertools import groupby
from typing import Any, AsyncGenerator, Iterable

from django.db.models.signals import post_save
from django.dispatch import receiver

from strawberry.types import Info
from strawberry_django_plus import gql

from src.apps.common.signals import post_bulk_save
from src.apps.documents import models

from . import types

Queue = asyncio.Queue[Iterable[models.Document]]

# TODO: Subscription support between multiple instances via messaging queues (CU-3wh6gmu)
# FIXME: Bad implementation without queue removal (limited possible cumulative overhead with maxsize to 10 for now)
queues: dict[int, Queue] = {}


@receiver(post_save, sender=models.Document)
def callback(
    sender: models.Document, instance: models.Document, *args: Any, created: bool, **kwargs: Any
) -> None:  # noqa: D103
    if not created:
        return

    queue = queues.setdefault(instance.folder.owner.id, asyncio.Queue[Iterable[models.Document]]())
    queue.put_nowait([instance])


@receiver(post_bulk_save, sender=models.Document)
def bulk_callback(
    sender: models.Document, instances: list[models.Document], *args: Any, created: bool, **kwargs: Any
) -> None:  # noqa: D103
    if not created:
        return

    for (owner_id, documents_group) in groupby(instances, key=lambda instance: instance.folder.owner.id):
        queue = queues.setdefault(owner_id, asyncio.Queue[Iterable[models.Document]]())
        queue.put_nowait(list(documents_group))


@gql.subscription
async def document_created(info: Info) -> AsyncGenerator[list[types.Document], None]:
    """Triggered new document created in user's folder."""
    user = info.context.request.scope["user"]
    if (queue := queues.get(user.id)) is None:
        queue = queues.setdefault(user.id, asyncio.Queue[Iterable[models.Document]](maxsize=10))

    while True:
        item = await queue.get()
        yield list(item)  # type: ignore[arg-type]
