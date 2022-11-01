from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from src.apps.common.admin import ModelAdmin

from . import forms, models
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
    readonly_fields = ("id", "last_modified")

    # List view
    # -----------------------------------------------------------------------------------------------------------------
    list_display = ("id", "username", "name", "is_staff", "is_superuser", "last_login", "date_joined")
    search_fields = ("name",)

    # Detail view
    # -----------------------------------------------------------------------------------------------------------------
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    fieldsets = (
        (
            None,
            {"fields": ("id", "username", "password")},
        ),
        (
            _("Personal info"),
            {"fields": ("name", "email")},
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "last_modified")},
        ),
    )


@admin.register(models.Token)
class TokenAdmin(ModelAdmin):
    readonly_fields = ("id", "created", "last_modified")

    # List view
    # -----------------------------------------------------------------------------------------------------------------
    list_display = ("id", "owner", "label", "valid_until", "created")
    search_fields = ("owner__username", "label")

    # Detail view
    # -----------------------------------------------------------------------------------------------------------------
    fieldsets = (
        (
            None,
            {"fields": ("id", "owner", "label")},
        ),
        (
            _("Details"),
            {"fields": ("key", "valid_until")},
        ),
        (
            _("Important dates"),
            {"fields": ("created", "last_modified")},
        ),
    )
    autocomplete_fields = ("owner",)
