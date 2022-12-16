from collections.abc import Iterable, Sequence
from typing import TypeVar

from django.db import models

from asgiref.sync import sync_to_async

from .signals import post_bulk_save

_T = TypeVar("_T", bound=models.Model)


# NOTE: Overridden type stubs are NOT necessarily correct, it is just for project internal use.


class QuerySet(models.QuerySet[_T]):
    pass


class Manager(models.Manager[_T]):
    """Extend default manager behavior with extra functionalities.

    Check out https://github.com/django/django/blob/main/django/db/models/query.py how override might affect to
    async ORM support.
    """

    model: type[_T]

    def get_queryset(self) -> QuerySet[_T]:
        return QuerySet(self.model, using=self._db)

    def bulk_create(  # type: ignore
        self,
        objs: Iterable[_T],
        batch_size: int | None = None,
        ignore_conflicts: bool = False,
        update_conflicts: bool = False,
        update_fields: Sequence[str] | None = None,
        unique_fields: Sequence[str] | None = None,
    ) -> list[_T]:
        """Overridden `bulk_create()` method to emit signal `post_bulk_save`."""
        instances = super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts,
            update_fields=update_fields,
            unique_fields=unique_fields,
        )
        post_bulk_save.send(self.model, instances=instances, created=True, using=self.db, update_fields=None)

        return instances

    async def abulk_create(  # type: ignore
        self,
        objs: Iterable[_T],
        batch_size: int | None = None,
        ignore_conflicts: bool = False,
        update_conflicts: bool = False,
        update_fields: Sequence[str] | None = None,
        unique_fields: Sequence[str] | None = None,
    ) -> list[_T]:
        return await sync_to_async(self.bulk_create)(  # type: ignore[no-any-return]
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_conflicts=update_conflicts,
            update_fields=update_fields,
            unique_fields=unique_fields,
        )

    def bulk_update(self, objs: Iterable[_T], fields: Sequence[str], batch_size: int | None = None) -> int:
        """Overridden `bulk_update()` method to emit signal `post_bulk_save`."""
        n = super().bulk_update(objs, fields, batch_size)
        post_bulk_save.send(self.model, instances=objs, created=False, using=self.db, update_fields=fields)

        return n

    async def abulk_update(self, objs: Iterable[_T], fields: Sequence[str], batch_size: int | None = None) -> int:
        return await sync_to_async(self.bulk_update)(objs, fields, batch_size)  # type: ignore[no-any-return]
