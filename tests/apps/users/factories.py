from datetime import timedelta
from typing import Any, Sequence

from django.utils import timezone

from factory import Faker, post_generation, SubFactory

from src.apps.users.models import Token, User
from tests.apps._helpers import ModelFactory


class UserFactory(ModelFactory[User]):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs: Any) -> None:
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ["username"]


class TokenFactory(ModelFactory[Token]):
    owner = SubFactory(UserFactory)
    label = Faker("pystr")
    valid_until = timezone.now() + timedelta(days=365)

    class Meta:
        model = Token
