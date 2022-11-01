from django.db import models
from django.db.models import functions
from django.utils.translation import gettext_lazy as _

from .managers import Manager

models.CharField.register_lookup(functions.Length, "length")


class Model(models.Model):
    created = models.DateTimeField(
        verbose_name=_("created at"), help_text=_("Creation datetime of folder."), editable=False, auto_now_add=True
    )
    last_modified = models.DateTimeField(
        verbose_name=_("last modified at"),
        help_text=_("Last modification datetime of folder."),
        editable=False,
        auto_now=True,
    )

    # ORM managers
    objects: Manager = Manager()

    class Meta:
        abstract = True
