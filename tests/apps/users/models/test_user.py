from django.contrib.auth import get_user_model

import pytest

from src.apps.users.models import User
from tests.apps._helpers import ModelTestBase

from ..factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUser(ModelTestBase):
    model_cls = User
    factory_cls = UserFactory

    def test_django_get_user_model_is_user(self) -> None:
        assert get_user_model() is User
