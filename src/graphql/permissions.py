from logging import getLogger
from typing import Any, TYPE_CHECKING

from strawberry.channels.context import StrawberryChannelsContext
from strawberry.permission import BasePermission
from strawberry.types import Info

from src.apps.users.models import Token, User

logger = getLogger(__name__)


class APIKey(BasePermission):
    """OAuth HTTP bearer authorization."""

    message = "Not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool:
        if TYPE_CHECKING:
            assert isinstance(info.context, StrawberryChannelsContext)

        authorization = info.context.request.headers.get("authorization")
        if authorization is None:
            scheme, credentials = "", ""
        else:
            scheme, credentials = authorization.split(" ")

        if scheme.lower() != "bearer":
            raise Exception(f"unsupported scheme: {scheme!r}")

        # Set user to scope for later use
        info.context.request.scope["user"] = await self.get_user(key=credentials)

        return True

    async def get_user(self, key: str) -> User:
        try:
            token: Token = await Token.objects.select_related("owner").aget(key=key)
        except Token.DoesNotExist:
            valid = False
        else:
            valid = token.is_valid()

        if not valid:
            raise Exception("Token is invalid or expired.")

        return token.owner
