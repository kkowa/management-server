from typing import Any, AsyncIterator, Iterable, MutableMapping, Sequence, Type, TYPE_CHECKING, TypeVar

from django.db import models

from asgiref.sync import sync_to_async

from .signals import post_bulk_save

_T = TypeVar("_T", bound=models.Model)


# NOTE: Overridden type stubs are NOT necessarily correct, it is just for project internal use.


class QuerySet(models.QuerySet[_T]):

    if TYPE_CHECKING:

        def get(self, *args: Any, **kwargs: Any) -> _T:
            ...

        async def aget(self, *args: Any, **kwargs: Any) -> _T:
            ...

        async def acreate(self, **kwargs: Any) -> _T:
            ...

        async def aget_or_create(
            self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any
        ) -> tuple[_T, bool]:
            ...

        async def aupdate_or_create(
            self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any
        ) -> tuple[_T, bool]:
            ...

        async def abulk_create(
            self, objs: Iterable[_T], batch_size: int | None = ..., ignore_conflicts: bool = False
        ) -> list[_T]:
            ...

        async def abulk_update(self, objs: Iterable[_T], fields: Sequence[str], batch_size: int | None = ...) -> int:
            ...

        async def acount(self) -> int:
            ...

        async def ain_bulk(self, id_list: Iterable[Any] | None = ..., *, field_name: str = ...) -> dict[Any, _T]:
            ...

        async def aiterator(self, chunk_size: int = ...) -> AsyncIterator[_T]:
            ...

        async def alatest(self, *fields: Any, field_name: Any | None = ...) -> _T:
            ...

        async def aearliest(self, *fields: Any, field_name: Any | None = ...) -> _T:
            ...

        async def afirst(self) -> _T | None:
            ...

        async def alast(self) -> _T | None:
            ...

        async def aaggregate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            ...

        async def aexists(self) -> bool:
            ...

        def contains(self, obj: _T) -> bool:  # Seems missing from django-stubs, maybe bug?
            ...

        async def acontains(self, obj: _T) -> bool:
            ...

        async def aupdate(self, **kwargs: Any) -> int:
            ...

        async def adelete(self) -> tuple[int, dict[str, int]]:
            ...

        async def aexplain(self, *, format: Any | None = ..., **options: Any) -> str:
            ...


class Manager(models.Manager[_T]):
    """Extend default manager behavior with extra functionalities.

    Check out https://github.com/django/django/blob/main/django/db/models/query.py how override might affect to
    async ORM support.
    """

    model: Type[_T]

    def get_queryset(self) -> QuerySet[_T]:
        return QuerySet(self.model, using=self._db)

    # Monkey-patch type stubs as django-stubs currently does not support this
    # NOTE: https://github.com/typeddjango/django-stubs/issues/1092
    if TYPE_CHECKING:

        def get(self, *args: Any, **kwargs: Any) -> _T:
            ...

        def none(self) -> QuerySet[_T]:
            ...

        def all(self) -> QuerySet[_T]:
            ...

        def filter(self, *args: Any, **kwargs: Any) -> QuerySet[_T]:
            ...

        def exclude(self, *args: Any, **kwargs: Any) -> QuerySet[_T]:
            ...

        def complex_filter(self, filter_obj: Any) -> QuerySet[_T]:
            ...

        def count(self) -> int:
            ...

        def union(self, *other_qs: Any, all: bool = ...) -> QuerySet[_T]:
            ...

        def intersection(self, *other_qs: Any) -> QuerySet[_T]:
            ...

        def difference(self, *other_qs: Any) -> QuerySet[_T]:
            ...

        def select_for_update(
            self, nowait: bool = ..., skip_locked: bool = ..., of: Sequence[str] = ..., no_key: bool = ...
        ) -> QuerySet[_T]:
            ...

        def select_related(self, *fields: Any) -> QuerySet[_T]:
            ...

        def prefetch_related(self, *lookups: Any) -> QuerySet[_T]:
            ...

        def annotate(self, *args: Any, **kwargs: Any) -> QuerySet[_T]:
            ...

        def alias(self, *args: Any, **kwargs: Any) -> QuerySet[_T]:
            ...

        def order_by(self, *field_names: Any) -> QuerySet[_T]:
            ...

        def distinct(self, *field_names: Any) -> QuerySet[_T]:
            ...

        def extra(
            self,
            select: dict[str, Any] | None = ...,
            where: list[str] | None = ...,
            params: list[Any] | None = ...,
            tables: list[str] | None = ...,
            order_by: Sequence[str] | None = ...,
            select_params: Sequence[Any] | None = ...,
        ) -> QuerySet[Any]:
            ...

        def reverse(self) -> QuerySet[_T]:
            ...

        def defer(self, *fields: Any) -> QuerySet[_T]:
            ...

        def only(self, *fields: Any) -> QuerySet[_T]:
            ...

        def using(self, alias: str | None = ...) -> QuerySet[_T]:
            ...

        async def aget(self, *args: Any, **kwargs: Any) -> _T:
            ...

        async def acreate(self, **kwargs: Any) -> _T:
            ...

        async def aget_or_create(
            self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any
        ) -> tuple[_T, bool]:
            ...

        async def aupdate_or_create(
            self, defaults: MutableMapping[str, Any] | None = ..., **kwargs: Any
        ) -> tuple[_T, bool]:
            ...

        async def acount(self) -> int:
            ...

        async def ain_bulk(self, id_list: Iterable[Any] | None = ..., *, field_name: str = ...) -> dict[Any, _T]:
            ...

        async def aiterator(self, chunk_size: int = ...) -> AsyncIterator[_T]:
            ...

        async def alatest(self, *fields: Any, field_name: Any | None = ...) -> _T:
            ...

        async def aearliest(self, *fields: Any, field_name: Any | None = ...) -> _T:
            ...

        async def afirst(self) -> _T | None:
            ...

        async def alast(self) -> _T | None:
            ...

        async def aaggregate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            ...

        async def aexists(self) -> bool:
            ...

        def contains(self, obj: _T) -> bool:  # Seems missing from django-stubs, maybe bug?
            ...

        async def acontains(self, obj: _T) -> bool:
            ...

        async def aupdate(self, **kwargs: Any) -> int:
            ...

        async def adelete(self) -> tuple[int, dict[str, int]]:
            ...

        async def aexplain(self, *, format: Any | None = ..., **options: Any) -> str:
            ...

    def bulk_create(
        self, objs: Iterable[_T], batch_size: int | None = None, ignore_conflicts: bool = False
    ) -> list[_T]:
        """Overridden `bulk_create()` method to emit signal `post_bulk_save`."""
        instances = super().bulk_create(objs, batch_size, ignore_conflicts)
        post_bulk_save.send(self.model, instances=instances, created=True, using=self.db, update_fields=None)

        return instances

    async def abulk_create(
        self, objs: Iterable[_T], batch_size: int | None = None, ignore_conflicts: bool = False
    ) -> list[_T]:
        return await sync_to_async(self.bulk_create)(objs, batch_size, ignore_conflicts)  # type: ignore[no-any-return]

    def bulk_update(self, objs: Iterable[_T], fields: Sequence[str], batch_size: int | None = None) -> int:
        """Overridden `bulk_update()` method to emit signal `post_bulk_save`."""
        n = super().bulk_update(objs, fields, batch_size)
        post_bulk_save.send(self.model, instances=objs, created=False, using=self.db, update_fields=fields)

        return n

    async def abulk_update(self, objs: Iterable[_T], fields: Sequence[str], batch_size: int | None = None) -> int:
        return await sync_to_async(self.bulk_update)(objs, fields, batch_size)  # type: ignore[no-any-return]
