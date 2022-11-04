"""ASGI config for kkowa project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""
import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application
from django.urls import re_path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from starlette.middleware.cors import CORSMiddleware

# This allows easy placement of apps within the interior src directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "src"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

# Django application MUST be setup earlier than any other applications if depends on Django features.
django_application = get_asgi_application()

# FastAPI; MUST after django has been setup (it depends on Django features)
from config.api import get_api_application  # noqa: E402

fastapi_application = get_api_application()

# Strawberry GraphQL
from strawberry.channels.handlers.http_handler import GraphQLHTTPConsumer  # noqa: E402
from strawberry.channels.handlers.ws_handler import GraphQLWSConsumer  # noqa: E402

from config.graphql import schema  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                re_path("^api", fastapi_application),  # type: ignore[arg-type]
                re_path(
                    "^graphql",
                    CORSMiddleware(  # type: ignore[arg-type]
                        GraphQLHTTPConsumer.as_asgi(schema=schema),
                        allow_origins=["*"],
                        allow_methods=["*"],
                        allow_headers=["*"],
                        allow_credentials=True,
                    ),
                ),
                re_path("^", django_application),  # type: ignore[arg-type]
            ]
        ),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        re_path("^graphql", GraphQLWSConsumer.as_asgi(schema=schema)),
                    ],
                )
            )
        ),
    }
)
