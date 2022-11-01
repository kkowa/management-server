from datetime import timedelta

from django.test.client import Client
from django.utils import timezone

import pytest
from fastapi import status

from src.apps.users.models import Token, User
from tests.apps._helpers import ModelAdminTestBase

from .factories import TokenFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestUserAdmin(ModelAdminTestBase):
    model_cls = User
    factory_cls = UserFactory

    def test_add(self, admin_client: Client) -> None:
        super().test_add(admin_client)

        url = self._get_url("add")
        response = admin_client.post(
            path=url,
            data={
                "username": "test",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert self.model_cls.objects.filter(username="test").exists()


class TestTokenAdmin(ModelAdminTestBase):
    model_cls = Token
    factory_cls = TokenFactory

    def test_add(self, admin_user: User, admin_client: Client) -> None:  # type: ignore[override]
        super().test_add(admin_client)

        url = self._get_url("add")
        valid_until = timezone.localtime(timezone.now() + timedelta(hours=1))
        response = admin_client.post(
            path=url,
            data={
                "owner": admin_user.id,
                "label": "test",
                "valid_until_0": valid_until.date(),
                "valid_until_1": valid_until.time(),
            },
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert self.model_cls.objects.filter(owner=admin_user, label="test").exists()
