from datetime import timedelta

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone

import pytest

from src.apps.users.models import Token
from tests.apps._helpers import ModelTestBase

from ..factories import TokenFactory

pytestmark = pytest.mark.django_db


class TestToken(ModelTestBase):
    model_cls = Token
    factory_cls = TokenFactory

    def test_instance_creation_constraint_valid_until_must_be_future(self) -> None:
        # NOTE: Test synchronously to handle transactions easily
        with transaction.atomic():
            with pytest.raises(IntegrityError, match=r'.* violates check constraint ".*_valid_until_must_be_future"'):
                self.factory_cls(valid_until=timezone.now() - timedelta(minutes=1))

        with transaction.atomic():
            with pytest.raises(IntegrityError, match=r'.* violates check constraint ".*_valid_until_must_be_future"'):
                self.factory_cls(valid_until=timezone.now())

        self.factory_cls(valid_until=timezone.now() + timedelta(minutes=1))

    def test__generate_token(self) -> None:
        # Test tokens are generated uniquely
        assert len({Token._generate_token() for _ in range(100)}) == 100

    async def test_save(self) -> None:
        token = await TokenFactory.acreate(key=None)
        assert token.key

    def test_is_valid(self) -> None:
        token = TokenFactory.build()
        assert token.is_valid()
