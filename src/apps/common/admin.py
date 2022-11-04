from typing import Any, Type

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

DEFAULT_HELP_TEXTS = {
    "id": _("Database primary key."),
}


class ModelAdmin(admin.ModelAdmin):
    """Project-specific custom model admin with extra features to `django.contrib.admin.ModelAdmin`."""

    help_texts: dict[str, str] | None = None

    def get_help_texts(self) -> dict[str, str]:
        """Return help texts."""
        if self.help_texts is None:
            return DEFAULT_HELP_TEXTS  # type: ignore[return-value]

        return DEFAULT_HELP_TEXTS | self.help_texts  # type: ignore[return-value]

    def get_form(self, *args: Any, **kwargs: Any) -> Type[forms.ModelForm]:
        """Apply extra features on admin forms."""
        form = super().get_form(*args, **kwargs)

        # Feature support for setting & overriding form help texts
        help_texts = self.get_help_texts()
        if isinstance(form._meta.help_texts, dict):
            form._meta.help_texts |= help_texts
        else:
            form._meta.help_texts = help_texts

        return form
