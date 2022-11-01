from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.api import dependencies
from src.api.routers import documents, users


def get_api_application(root_prefix: str = "/api") -> FastAPI:
    """Create new FastAPI application."""
    application = FastAPI(
        openapi_url=f"{root_prefix}/openapi.json",
        docs_url=f"{root_prefix}/docs",
        redoc_url=f"{root_prefix}/redoc",
        dependencies=[Depends(dependencies.APIKey())],
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "https://localhost", "http://localhost:*", "https://localhost:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup routers
    router = APIRouter(prefix="/api")
    router.include_router(users.router)
    router.include_router(documents.router)

    # Install root router
    application.include_router(router)

    # Extend OpenAPI
    openapi_schema = get_openapi(
        title="kkowa Open API",
        version="0.1.0",
        description="""
This page is automatically generated documentation of kkowa server's Open API.

Features are support by GraphQL. API is designed for communication between organization components to perform simple
tasks with simple HTTP calls only.
Advanced users may also use this API using their API keys to build their own programs.

For more information not described in this page, please contact organization or project administrators or maintainers.
    """,
        terms_of_service="",
        contact={},
        license_info={},
        routes=application.routes,
    )

    # TODO: Use custom logo
    # openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}

    # TODO: Change page title
    # ...

    application.openapi_schema = openapi_schema

    return application
