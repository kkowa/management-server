import pytest

from src.apps.documents.models import Document
from tests.apps._helpers import ModelTestBase

from ..factories import DocumentFactory

pytestmark = pytest.mark.django_db


class TestDocument(ModelTestBase):
    """Test `Document` model."""

    model_cls = Document
    factory_cls = DocumentFactory

    def test_type(self) -> None:
        # Ordinary types JSON serializable
        tests = [
            ("lorem ipsum", "string"),
            ("", "string"),
            (True, "boolean"),
            (False, "boolean"),
            (1, "number"),
            (0, "number"),
            (-1, "number"),
            (1.0, "number"),
            (0.0, "number"),
            (-1.0, "number"),
            ({"key": "value"}, "object"),
            ({}, "object"),
            (["element"], "array"),
            ([], "array"),
            (None, "null"),
        ]
        for (data, expect) in tests:
            document = DocumentFactory.build(data=data)
            result = document.type()
            assert result == expect, f"for {data!r}, expected {expect!r} but got: {result!r}"

        # Python objects are unacceptable
        with pytest.raises(NotImplementedError):
            document.data = object()
            document.type()
