import json

from django.test import Client

import pytest
from fastapi import status

from src.apps.documents.models import Document, Folder
from src.apps.users.models import User
from tests.apps._helpers import ModelAdminTestBase

from .factories import DocumentFactory, FolderFactory

pytestmark = pytest.mark.django_db


class TestFolderAdmin(ModelAdminTestBase):
    """Test `FolderAdmin`."""

    model_cls = Folder
    factory_cls = FolderFactory

    def test_add(self, admin_user: User, admin_client: Client) -> None:  # type: ignore[override]
        super().test_add(admin_client)

        url = self._get_url("add")
        response = admin_client.post(
            path=url,
            data={
                "owner": admin_user.id,
                "name": "test",
            },
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert self.model_cls.objects.filter(owner=admin_user, name="test").exists()


class TestDocumentAdmin(ModelAdminTestBase):
    """Test `DocumentAdmin`."""

    model_cls = Document
    factory_cls = DocumentFactory

    def test_add(self, admin_user: User, admin_client: Client) -> None:  # type: ignore[override]
        super().test_add(admin_client)

        url = self._get_url("add")
        folder = FolderFactory(owner=admin_user)
        response = admin_client.post(
            path=url,
            data={
                "folder": folder.id,
                "data": json.dumps("test"),
            },
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert self.model_cls.objects.get(folder=folder).data == "test"
