import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_users_me(admin_client: TestClient) -> None:  # noqa: D103
    response = admin_client.get(url="/api/users/me")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK, data
    assert "password" not in data
