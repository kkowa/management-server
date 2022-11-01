from factory import Faker, SubFactory

from src.apps.documents.models import Document, Folder
from tests.apps._helpers import ModelFactory
from tests.apps.users.factories import UserFactory


class FolderFactory(ModelFactory[Folder]):
    owner = SubFactory(UserFactory)
    name = Faker("word")

    class Meta:
        model = Folder


class DocumentFactory(ModelFactory[Document]):
    folder = SubFactory(FolderFactory)
    data = Faker("json")

    class Meta:
        model = Document
