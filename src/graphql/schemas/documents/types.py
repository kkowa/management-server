from __future__ import annotations

from strawberry import auto
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

import src.graphql.schemas.users.types
from src.apps.documents import models


@gql.django.type(model=models.Folder)
class Folder(relay.Node):
    """Folder type to group documents."""

    id: auto
    owner: src.graphql.schemas.users.types.User
    name: auto
    created: auto
    last_modified: auto

    documents: relay.Connection[Document] = gql.django.connection()


@gql.django.type(model=models.Document)
class Document(relay.Node):
    """Document type to describe a collected data."""

    id: auto
    folder: Folder
    data: auto
    created: auto
    last_modified: auto
