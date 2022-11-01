from __future__ import annotations

import pytest
from asgiref.sync import sync_to_async

from src.apps.documents.models import Document
from src.apps.users.models import User
from tests.apps.documents.factories import DocumentFactory, FolderFactory
from tests.graphql._helpers import GraphQLClient, GraphQLTestBase

pytestmark = pytest.mark.integration


class TestDocumentSubscriptions(GraphQLTestBase):
    async def test_document_created(self, admin_user: User, admin_client: GraphQLClient) -> None:
        """Test subscription `document_created` for `post_save` signal."""
        folder = await FolderFactory.acreate(owner=admin_user, name="test")

        sub = admin_client.subscribe(
            query="""
            subscription {
                documentCreated {
                    id
                    folder {
                        name
                        owner {
                            username
                        }
                    }
                    data
                }
            }
            """,
        )

        # Trigger subscription event via `post_save` signal
        document = await DocumentFactory.acreate(folder=folder)
        result = await anext(sub)

        # Other users' document shouldn't trigger
        await DocumentFactory.acreate()
        with pytest.raises(StopAsyncIteration):
            await anext(sub)

        assert result.errors is None
        assert (data := result.data)
        assert len(data["documentCreated"]) == 1

        global_id = data["documentCreated"][0]["id"]
        id = self._resolve_global_id(global_id)
        assert await Document.objects.aget(id=id) == document

    async def test_document_created_bulk(self, admin_user: User, admin_client: GraphQLClient) -> None:
        """Test subscription `document_created` for `post_bulk_save` signal."""
        folder = await FolderFactory.acreate(owner=admin_user)

        sub = admin_client.subscribe(
            query="""
            subscription {
                documentCreated {
                    id
                    folder {
                        name
                        owner {
                            username
                        }
                    }
                    data
                }
            }
            """,
        )

        # Trigger subscription event via `post_bulk_save` signal
        documents = await Document.objects.abulk_create(DocumentFactory.build_batch(size=2, folder=folder))
        result = await anext(sub)

        # Other users' document shouldn't trigger
        await DocumentFactory.acreate_batch(size=3)
        with pytest.raises(StopAsyncIteration):
            await anext(sub)

        assert result.errors is None
        assert (data := result.data)
        assert len(data["documentCreated"]) == 2

        global_ids = [document["id"] for document in data["documentCreated"]]
        ids = (self._resolve_global_id(global_id) for global_id in global_ids)
        qs = Document.objects.filter(id__in=ids)
        assert await sync_to_async(list)(qs) == documents
