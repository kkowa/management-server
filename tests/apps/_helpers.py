from typing import Any, Generic, TYPE_CHECKING, TypeVar

from django.db import models
from django.db.models import Model
from django.test.client import Client
from django.urls import reverse

from asgiref.sync import sync_to_async
from factory.django import DjangoModelFactory
from fastapi import status

_T = TypeVar("_T", bound=models.Model)


class ModelFactory(DjangoModelFactory, Generic[_T]):
    """Custom Django model factory with extra features such as async interface support."""

    # Monkey-patch type annotations
    if TYPE_CHECKING:

        @classmethod
        def build(cls, **kwargs: Any) -> _T:
            ...

        @classmethod
        def build_batch(cls, size: int, **kwargs: Any) -> list[_T]:
            ...

    @classmethod
    async def acreate(cls, **kwargs: Any) -> _T:
        return await sync_to_async(cls.create)(**kwargs)  # type: ignore

    @classmethod
    async def acreate_batch(cls, size: int, **kwargs: Any) -> list[_T]:
        return await sync_to_async(cls.create_batch)(size=size, **kwargs)  # type: ignore


class ModelTestBase:
    """Base test template for models."""

    model_cls: type[Model]
    factory_cls: type[ModelFactory]

    # ======================================================================
    # Basic tests
    # ======================================================================
    async def test_instance_creation(self) -> None:
        """Test model instance can be created normally."""
        instance = await self.factory_cls.acreate()
        assert isinstance(instance, self.model_cls)


class ModelAdminTestBase:
    """Base test template for admins."""

    model_cls: type[Model]
    factory_cls: type[ModelFactory]

    # ======================================================================
    # Helper methods
    # ======================================================================
    @classmethod
    def _get_full_name(cls) -> str:
        """Returns "{app_label}_{model_name}" for use with `django.urls.reverse` to get page url."""
        app_label = cls.model_cls._meta.app_label
        model_name = cls.model_cls._meta.model_name
        return f"{app_label}_{model_name}"

    @classmethod
    def _get_url(cls, action: str, *, kwargs: dict[str, Any] | None = None) -> str:
        """Returns URL for admin action view."""
        return reverse(f"admin:{cls._get_full_name()}_{action}", kwargs=kwargs)

    # ======================================================================
    # Basic tests
    # ======================================================================
    def test_changelist(self, admin_client: Client) -> None:
        """Test model admin's changelist page."""
        url = self._get_url("changelist")
        response = admin_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

    def test_add(self, admin_client: Client) -> None:
        """Test model admin's add page is accessible. To test create instance via admin, override it.

        NOTE: Some form fields such as for `DateTimeField` consists of multiple fields (date, time).
              Check DDT request panel in development server for required body schema.

        NOTE: Be aware that POSTing date and time will be naive format (timezone cut off)
        """
        url = self._get_url("add")
        response = admin_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

    def test_view(self, admin_client: Client) -> None:
        """Test model admin's instance view page."""
        instance = self.factory_cls.create()
        url = self._get_url("change", kwargs={"object_id": instance.id})
        response = admin_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, admin_client: Client) -> None:
        """Test model admin instance deletion."""
        instance = self.factory_cls.create()
        url = self._get_url("delete", kwargs={"object_id": instance.id})

        # Test delete page is accessible
        response = admin_client.get(path=url)
        assert response.status_code == status.HTTP_200_OK

        # Test actual deletion operation
        response = admin_client.delete(path=url)
        assert response.status_code == status.HTTP_200_OK
