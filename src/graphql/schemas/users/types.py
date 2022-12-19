from strawberry import auto, LazyType
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

from src.apps.users import models


@gql.django.type(models.User)
class User(relay.Node):
    """Common user type."""

    id: auto
    username: auto
    name: auto
    date_joined: auto
    last_modified: auto

    folders: relay.Connection[  # type: ignore[type-var, name-defined]
        LazyType[
            "Folder", "src.graphql.schemas.documents.types"  # pyright: ignore[reportUndefinedVariable]  # noqa: F821
        ]
    ] = gql.django.connection()
