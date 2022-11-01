import pytest
from asgiref.sync import sync_to_async

from src.apps.users.models import User
from tests.apps.documents.factories import DocumentFactory, FolderFactory
from tests.graphql._helpers import GraphQLClient, GraphQLTestBase

pytestmark = pytest.mark.integration


class TestDocumentQueries(GraphQLTestBase):
    async def test_folders(self, admin_user: User, admin_client: GraphQLClient) -> None:
        folders = await FolderFactory.acreate_batch(size=2, owner=admin_user)
        await FolderFactory.acreate_batch(size=3)

        result = await admin_client.execute(
            query="""
            {
                folders {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
            """,
        )
        assert result.errors is None
        assert (data := result.data)

        global_ids = [edge["node"]["id"] for edge in data["folders"]["edges"]]
        ids = (self._resolve_global_id(global_id) for global_id in global_ids)
        qs = admin_user.folders.filter(id__in=ids).order_by("id")
        assert await sync_to_async(list)(qs) == folders

    async def test_documents(self, admin_user: User, admin_client: GraphQLClient) -> None:
        documents = await DocumentFactory.acreate_batch(
            size=2,
            folder=await FolderFactory.acreate(owner=admin_user),
        )
        await DocumentFactory.acreate_batch(size=3)

        result = await admin_client.execute(
            query="""
            {
                documents {
                    edges {
                        node {
                            id
                            folder {
                                name
                            }
                            data
                        }
                    }
                }
            }
            """,
        )
        assert result.errors is None
        assert (data := result.data)

        global_ids = [edge["node"]["id"] for edge in data["documents"]["edges"]]
        ids = (self._resolve_global_id(global_id) for global_id in global_ids)
        qs = (await admin_user.folders.aget()).documents.filter(id__in=ids)  # type: ignore[attr-defined]
        assert await sync_to_async(list)(qs) == documents
