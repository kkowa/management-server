from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.apps.users.models import Token, User


class APIKey(HTTPBearer):  # TODO: Write tests
    def __init__(self) -> None:  # noqa: D107
        super().__init__(
            description="Authenticate via API key.",
            auto_error=True,
        )

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Required credentials not provided.")

        # Set user to scope for later use
        request.scope["user"] = await self.get_user(key=credentials.credentials)

        return credentials

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
