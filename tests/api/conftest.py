import pytest
from fastapi.testclient import TestClient

from config.asgi import application
from src.apps.users.models import User
from tests.apps.users.factories import TokenFactory

# NOTE: NO-OP database changes seems not shared across test and application contexts for some reason.
#       FastAPI tests should be marked with `django_db(transaction=True)` or integration to make real transactions.


@pytest.fixture
def client() -> TestClient:
    """Create new FastAPI test client."""
    return TestClient(application)


@pytest.fixture
def admin_client(admin_user: User) -> TestClient:
    """Create new FastAPI test client authenticated as admin user."""
    token = TokenFactory(owner=admin_user)

    client = TestClient(application)
    client.headers = {
        "Authorization": f"Bearer {token.key}",
    }

    return client
