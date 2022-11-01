from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from src.apps.common.admin import ModelAdmin

from . import models


@admin.register(models.Folder)
class FolderAdmin(ModelAdmin):
    readonly_fields = ("id", "count", "created", "last_modified")
    help_texts = {
        "count": _("Number of documents in folder."),
    }

    # List view
    # -----------------------------------------------------------------------------------------------------------------
    list_display = ("id", "owner", "name", "count", "created", "last_modified")
    search_fields = ("name",)

    # Detail view
    # -----------------------------------------------------------------------------------------------------------------
    fieldsets = (
        (
            None,
            {"fields": ("id", "owner", "name", "count")},
        ),
        (
            _("Important dates"),
            {"fields": ("created", "last_modified")},
        ),
    )
    autocomplete_fields = ("owner",)

    # NOTE: Not adding document inline as it is too many

    def count(self, obj: models.Folder) -> int:
        return obj.documents.count()


@admin.register(models.Document)
class DocumentAdmin(ModelAdmin):
    readonly_fields = ("id", "type", "created", "last_modified")
    help_texts = {
        "type": _("JSON type of data."),
    }

    # List view
    # -----------------------------------------------------------------------------------------------------------------
    list_display = ("id", "folder", "type", "created", "last_modified")
    search_fields = ("folder__name", "folder__owner__username")

    # Detail view
    # -----------------------------------------------------------------------------------------------------------------
    fieldsets = (
        (
            None,
            {"fields": ("id", "folder", "type")},
        ),
        (
            _("Details"),
            {
                "classes": ("collapse",),
                "fields": ("data",),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("created", "last_modified")},
        ),
    )
    autocomplete_fields = ("folder",)
