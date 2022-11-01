from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["Users"])


class User(BaseModel):
    """Basic user schema."""

    username: str
    email: EmailStr
    date_joined: datetime
    last_login: datetime | None

    class Config:
        orm_mode = True


@router.get(
    path="/me",
    summary="Retrieve current user's info",
    response_model=User,
)
async def users_me(request: Request) -> User:
    """Returns user's info, who sending this request."""
    return User.from_orm(request.user)
