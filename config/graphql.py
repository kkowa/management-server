"""Define project GraphQL schemas.

Notes:
    - Type of `context` attribute in `graphene.ResolveInfo` differ depending on request handlers (ASGI, WebSocket, ...):

        - ASGI: `django.core.handlers.asgi.ASGIRequest` with extra attributes such as `user` set by middleware

        - WebSocket: `dict`, maybe Channels' connection scope with extra keys set by middleware

            {
                "type": "websocket",
                "path": "/subscriptions",
                "query_string": b"",
                "headers": [],
                "subprotocols": ["graphql-ws"],
                "cookies": {},
                "session": "<django.utils.functional.LazyObject object at ...>",
                "user": "<channels.auth.UserLazyObject object at ...>",
                "path_remaining": "",
                "url_route": {"args": (), "kwargs": {}},
            }

"""
import strawberry
from strawberry.field import StrawberryField
from strawberry.tools import create_type
from strawberry_django_plus.directives import SchemaDirectiveExtension

from src.graphql import permissions
from src.graphql.schemas.documents.mutations import create_documents
from src.graphql.schemas.documents.queries import documents, folders
from src.graphql.schemas.documents.subscriptions import document_created
from src.graphql.schemas.users.queries import user_self

# Gather all operations to apply patches
queries: list[StrawberryField] = [user_self, folders, documents]
mutations: list[StrawberryField] = [create_documents]
subscriptions: list[StrawberryField] = [document_created]  # type: ignore[list-item]

# Patch permissions to all operations
# NOTE: Strawberry currently uses old GraphiQL that does not supports header editor. It is WIP feature but until then,
#       use browser header editors or other GraphQL clients.
# See: https://github.com/strawberry-graphql/strawberry/issues/2071
operations: list[StrawberryField] = queries + mutations + subscriptions
for field in operations:
    field.permission_classes.extend((permissions.APIKey,))

# Create operations
Query = create_type("Query", queries)
Mutation = create_type("Mutation", mutations)
Subscription = create_type("Subscription", subscriptions)

# Build schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    extensions=[
        SchemaDirectiveExtension,
    ],
)
