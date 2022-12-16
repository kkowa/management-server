from __future__ import annotations

from typing import TYPE_CHECKING

from strawberry import auto, LazyType
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

from src.apps.users import models

if TYPE_CHECKING:
    from src.graphql.schemas.documents.types import Folder


@gql.django.type(models.User)
class User(relay.Node):
    """Common user type."""

    id: auto
    username: auto
    name: auto
    date_joined: auto
    last_modified: auto

    folders: relay.Connection[  # type: ignore[type-var, name-defined]
        LazyType["Folder", "src.graphql.schemas.documents.types"]  # noqa: F821
    ] = gql.django.connection()
