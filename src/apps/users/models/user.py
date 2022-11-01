from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AbstractUserManager
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from src.apps.common.managers import Manager
from src.apps.common.models import Model

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from src.apps.documents.models import Folder

    from .token import Token


class UserManager(AbstractUserManager, Manager["User"]):
    pass


class User(AbstractUser, Model):
    """Default user for kkowa."""

    # First and last name do not cover name patterns around the globe
    name = CharField(verbose_name=_("name of user"), help_text=_("User's real name."), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    # `date_joined` already do the same
    created = None  # type: ignore[assignment]

    # Relation type stubs
    tokens: RelatedManager[Token]
    folders: RelatedManager[Folder]

    # ORM managers
    objects: UserManager = UserManager()
