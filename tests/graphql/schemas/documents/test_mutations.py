import pytest
from asgiref.sync import sync_to_async

from src.apps.documents.models import Document
from src.apps.users.models import User
from tests.graphql._helpers import GraphQLClient, GraphQLTestBase

pytestmark = pytest.mark.integration


class TestDocumentMutations(GraphQLTestBase):
    async def test_create_documents(self, admin_user: User, admin_client: GraphQLClient) -> None:
        result = await admin_client.execute(
            query="""
            mutation m($input: CreateDocumentsInput!) {
                createDocuments(input: $input) {
                    documents {
                        id
                        folder {
                            owner {
                                username
                            }
                            name
                        }
                        data
                    }
                }
            }
            """,
            variables={
                "input": {
                    "documents": [
                        {
                            "folder": "test-1",
                            "data": {"x": 9, "y": -17.21},
                        },
                        {
                            "folder": "test-1",
                            "data": "lorem ipsum",
                        },
                        {
                            "folder": "test-2",
                            "data": False,
                        },
                    ],
                }
            },
        )
        assert result.errors is None
        assert await sync_to_async(list)(
            Document.objects.filter(folder__owner=admin_user).values("folder__name", "data")
        ) == [
            {"folder__name": "test-1", "data": {"x": 9, "y": -17.21}},
            {"folder__name": "test-1", "data": "lorem ipsum"},
            {"folder__name": "test-2", "data": False},
        ]
