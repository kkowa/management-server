import pytest

from src.apps.documents.models import Folder
from tests.apps._helpers import ModelTestBase

from ..factories import FolderFactory

pytestmark = pytest.mark.django_db


class TestFolder(ModelTestBase):
    """Test `Folder` model."""

    model_cls = Folder
    factory_cls = FolderFactory
