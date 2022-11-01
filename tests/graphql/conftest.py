import pytest

from src.apps.users.models import User
from tests.apps.users.factories import TokenFactory

from ._helpers import GraphQLClient


@pytest.fixture
def client() -> GraphQLClient:
    """Create new GraphQL client."""
    return GraphQLClient()


@pytest.fixture
async def admin_client(admin_user: User) -> GraphQLClient:
    """Create new GraphQL client with authorized as admin user."""
    token = await TokenFactory.acreate(owner=admin_user)

    return GraphQLClient(
        headers={
            "Authorization": f"Bearer {token.key}",
        }
    )
