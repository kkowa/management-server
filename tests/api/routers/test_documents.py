import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.apps.users.models import User
from tests.apps.documents.factories import FolderFactory

pytestmark = pytest.mark.integration


@pytest.mark.parametrize(
    "existing_folders",  # Folders that should exists before API call
    [
        [],
        ["uncategorized"],
        ["uncategorized", "mobile"],
    ],
)
def test_create_documents(
    admin_user: User, admin_client: TestClient, existing_folders: list[str]
) -> None:  # noqa: D103
    for folder in existing_folders:
        FolderFactory(owner=admin_user, name=folder)

    response = admin_client.post(
        url="/api/documents",
        json=[
            {"folder": "uncategorized", "data": {"x": 11.52, "y": -43}},
            {"folder": "mobile", "data": {"kind": "error", "description": "lorem ipsum", "extra": None}},
        ],
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED, data
    assert len(data) == 2
    assert all(item.keys() == {"id"} for item in data)
