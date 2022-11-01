from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import Model
from src.apps.users.models import User

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

    from .document import Document


class Folder(Model):
    """Folder to group documents."""

    owner = models.ForeignKey["Folder", User](
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        help_text=_("Folder's owner."),
        related_name="folders",
        on_delete=models.CASCADE,
    )
    name = models.CharField(verbose_name=_("name of folder"), help_text=_("Name of folder to display."), max_length=50)

    # Relation type stubs
    documents: RelatedManager[Document]

    class Meta:
        verbose_name = _("folder")
        verbose_name_plural = _("folders")
        constraints = (
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_per_user",
                fields=("owner", "name"),
            ),
        )
        ordering = ("name", "created")

    def __str__(self) -> str:
        return f"{self.owner}/{self.name}"
