from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    """App configuration for documents."""

    name = "src.apps.documents"
    verbose_name = _("Documents")
