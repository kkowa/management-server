from django.db import models, transaction
from django.db.models.fields.json import JSONField
from django.utils.translation import gettext_lazy as _

from src.apps.common.managers import Manager
from src.apps.common.models import Model
from src.apps.users.models import User

from .. import datamodels
from .folder import Folder


class DocumentManager(Manager["Document"]):
    def create_documents_with_folders(
        self, owner: User, input: list[datamodels.CreateDocumentInput]
    ) -> list["Document"]:
        with transaction.atomic():
            folder_names = {document.folder for document in input}

            # Check all folders exists
            folders = list(Folder.objects.filter(owner=owner, name__in=folder_names))

            # List folders not exist
            folders_to_create = folder_names - set(folder.name for folder in folders)

            # Create folders does not exists
            # NOTE: Do not use `ignore_conflicts=True` as it does not return PK of created instances
            if folders_to_create:
                folders.extend(
                    Folder.objects.bulk_create(
                        (
                            Folder(
                                owner=owner,
                                name=name,
                            )
                            for name in folders_to_create
                        )
                    )
                )

            # Fetch bulk-created folders from DB
            # NOTE: Can't use returned list from `bulk_create()` due to:z
            #       "bulk_create() prohibited to prevent data loss due to unsaved related object ..."
            folders_map = {folder.name: folder for folder in folders}

            # Create bulk of documents
            documents = Document.objects.bulk_create(
                (
                    Document(
                        **(
                            document.dict()
                            | {
                                "folder": folders_map[document.folder],
                            }
                        )
                    )
                    for document in input
                )
            )

        return documents


class Document(Model):
    """Data document model received from various sources."""

    folder = models.ForeignKey["Document", Folder](
        to=Folder,
        verbose_name=_("folder"),
        help_text=_("Document folder it belongs to."),
        related_name="documents",
        on_delete=models.CASCADE,
    )
    data = JSONField(verbose_name=_("data"), help_text=_("Document data in JSON format."), null=True, blank=True)

    # ORM managers
    objects: DocumentManager = DocumentManager()

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ("created",)

    def __str__(self) -> str:
        return f"{self.folder}/{self.id}"

    def type(self) -> str:
        """Return type of data."""
        match self.data:
            case str():
                return "string"
            case bool():
                return "boolean"
            case int() | float():
                return "number"
            case dict():
                return "object"
            case list():
                return "array"
            case None:
                return "null"
            case undefined:
                raise NotImplementedError('can\'t stringify type "{!r}" into JSON type string', undefined)
