from __future__ import annotations

from strawberry.types import Info
from strawberry_django_plus import gql

from . import types


@gql.field
async def user_self(info: Info) -> types.User:
    """Return current user information."""
    return info.context.request.scope["user"]  # type: ignore[no-any-return]
