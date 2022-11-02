from __future__ import annotations

from strawberry import auto
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

import src.graphql.schemas.documents.types
from src.apps.users import models


@gql.django.type(models.User)
class User(relay.Node):
    """Common user type."""

    id: auto
    username: auto
    name: auto
    date_joined: auto
    last_modified: auto

    folders: relay.Connection[src.graphql.schemas.documents.types.Folder] = gql.django.connection()
