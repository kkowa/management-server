from __future__ import annotations

import secrets
from collections.abc import Iterable
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import functions
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import Model

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Token(Model):
    """User token model."""

    owner = models.ForeignKey["Token", "User"](
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("token owner"),
        help_text=_("Token's owner."),
        related_name="tokens",
        on_delete=models.CASCADE,
    )
    label = models.CharField(
        verbose_name=_("label"),
        help_text=_("User custom label for token for identification."),
        max_length=50,
        blank=True,
    )
    key = models.CharField(
        verbose_name=_("key"), help_text=_("Value of token."), unique=True, max_length=255, blank=True
    )
    valid_until = models.DateTimeField(verbose_name=_("valid until"), help_text=_("Datetime when token expires."))

    # TODO: Scopes
    # scopes = ArrayField(models.CharField(...), ...)

    class Meta:
        verbose_name = _("token")
        verbose_name_plural = _("tokens")
        ordering = ("label",)
        constraints = (
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_valid_until_must_be_future",
                check=models.Q(valid_until__gt=functions.Now()),
            ),
        )

    @classmethod
    def _generate_token(cls) -> str:
        """Generate cryptographically strong random token.

        See: https://docs.python.org/3/library/secrets.html
        """
        return secrets.token_urlsafe(nbytes=20)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        # Generate token if not set
        if not self.key:
            self.key = self._generate_token()

        return super().save(force_insert, force_update, using, update_fields)

    def is_valid(self) -> bool:
        return timezone.now() <= self.valid_until

    def __str__(self) -> str:
        return f"{self.owner!s}/{self.label or self.id}"
