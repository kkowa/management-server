import pytest

from src.apps.users import models
from tests.graphql._helpers import GraphQLClient, GraphQLTestBase

pytestmark = pytest.mark.integration


class TestUserQueries(GraphQLTestBase):
    async def test_user_self(self, admin_user: models.User, admin_client: GraphQLClient) -> None:
        result = await admin_client.execute(
            query="""
            {
                userSelf {
                    id
                    username
                }
            }
            """,
        )
        assert result.errors is None
        assert (data := result.data)

        global_id = data["userSelf"]["id"]
        id = self._resolve_global_id(global_id)
        assert await models.User.objects.aget(id=id) == admin_user
