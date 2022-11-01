from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """App configuration for users."""

    name = "src.apps.users"
    verbose_name = _("Users")
