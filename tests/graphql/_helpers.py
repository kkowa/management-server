from __future__ import annotations

import json
from typing import Any, AsyncGenerator
from uuid import uuid4

from channels.testing import HttpCommunicator, WebsocketCommunicator
from strawberry_django_plus.gql import relay

from config.asgi import application
from graphql import ExecutionResult


class GraphQLTestBase:
    """Base test template GraphQL operations."""

    # ======================================================================
    # Helper methods
    # ======================================================================
    @classmethod
    def _resolve_global_id(self, global_id: str) -> Any:
        """Resolve database ID from given global ID."""
        _, id = relay.from_base64(global_id)
        return id


class GraphQLClient:
    """Simple GraphQL subscription client over websocket."""

    timeout = 3

    def __init__(self, headers: dict[str, str] | None = None) -> None:
        """Create new GraphQL client."""
        if headers is None:
            headers = {}

        self.headers = headers

    async def execute(
        self, query: str, variables: dict[str, Any] | None = None, operation_name: str | None = None
    ) -> ExecutionResult:
        comm = HttpCommunicator(
            application=application,
            method="POST",
            path="/graphql",
            headers=[(key.encode(), value.encode()) for (key, value) in self.headers.items()],
            body=json.dumps(
                {
                    "query": query,
                    "variables": variables,
                    "operationName": operation_name,
                }
            ).encode(),
        )

        response = await comm.get_response(timeout=self.timeout)
        assert (status := response["status"]) == 200, f"unexpected status code: ${status!r}"

        payload = json.loads(response["body"])
        return ExecutionResult(data=payload.get("data"), errors=payload.get("errors"))

    async def subscribe(
        self, query: str, variables: dict[str, Any] | None = None, operation_name: str | None = None
    ) -> AsyncGenerator[ExecutionResult, None]:
        comm = WebsocketCommunicator(
            application=application,
            path="/graphql",
            headers=[(key.encode(), value.encode()) for (key, value) in self.headers.items()],
            subprotocols=["graphql-ws"],
        )

        subscription_id = str(uuid4())
        payload: dict[str, Any] = {
            "query": query,
            "variables": variables,
            "operationName": operation_name,
        }

        assert (conn := await comm.connect(timeout=self.timeout)) == (
            True,
            "graphql-ws",
        ), f"failed to establish connection: {conn!r}"

        try:
            # Subprotocol init
            await comm.send_json_to(
                {
                    "type": "connection_init",
                    "payload": {},
                }
            )
            assert (ack := await comm.receive_json_from(timeout=self.timeout)) == {
                "type": "connection_ack"
            }, f"failed to initialize GraphQL subprotocol, but: {ack!r}"

            await comm.send_json_to(
                {
                    "type": "start",
                    "id": subscription_id,
                    "payload": payload,
                }
            )

            while True:
                result = await comm.receive_json_from(timeout=self.timeout)
                match result["type"]:
                    case "data" | "error":
                        payload = result["payload"]
                        yield ExecutionResult(data=payload.get("data"), errors=payload.get("errors"))

                    case unknown:
                        raise NotImplementedError(f"unhandled type {unknown!r} caught")

        except Exception:
            await comm.disconnect(timeout=self.timeout)
