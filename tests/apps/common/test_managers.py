from unittest import mock

import pytest

from src.apps.common.signals import post_bulk_save
from src.apps.users.models import User
from tests.apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestManager:
    def test_bulk_create(self) -> None:
        """Test `.bulk_create()` method emits signal `post_bulk_save`."""
        handler = mock.MagicMock()
        post_bulk_save.connect(handler, sender=User)

        instances = User.objects.bulk_create(UserFactory.build_batch(size=3))

        handler.assert_called_once_with(
            signal=post_bulk_save, sender=User, instances=instances, created=True, using="default", update_fields=None
        )

    async def test_abulk_create(self) -> None:
        handler = mock.MagicMock()
        post_bulk_save.connect(handler, sender=User)

        instances = await User.objects.abulk_create(UserFactory.build_batch(size=3))

        handler.assert_called_once_with(
            signal=post_bulk_save, sender=User, instances=instances, created=True, using="default", update_fields=None
        )

    def test_bulk_update(self) -> None:
        """Test `.bulk_update()` method emits signal `post_bulk_save`."""
        handler = mock.MagicMock()
        post_bulk_save.connect(handler, sender=User)

        instances = UserFactory.create_batch(size=3)
        for instance in instances:
            instance.username = "__" + instance.username

        User.objects.bulk_update(instances, fields=["username"])

        handler.assert_called_once_with(
            signal=post_bulk_save,
            sender=User,
            instances=instances,
            created=False,
            using="default",
            update_fields=["username"],
        )

    async def test_abulk_update(self) -> None:
        handler = mock.MagicMock()
        post_bulk_save.connect(handler, sender=User)

        instances = await UserFactory.acreate_batch(size=3)
        for instance in instances:
            instance.username = "__" + instance.username

        await User.objects.abulk_update(instances, fields=["username"])

        handler.assert_called_once_with(
            signal=post_bulk_save,
            sender=User,
            instances=instances,
            created=False,
            using="default",
            update_fields=["username"],
        )
