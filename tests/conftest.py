import asyncio
import json
from collections.abc import Generator
from enum import Enum
from pathlib import Path
from typing import Any

from django.conf import LazySettings

import py
import pytest
from _pytest.config import Config
from _pytest.fixtures import SubRequest
from _pytest.mark.structures import Mark
from _pytest.python import Function
from pytest_socket import disable_socket

# =============================================================================
# Global test configurations
# =============================================================================
# https://docs.pytest.org/en/latest/reference/reference.html#hooks
# TODO: Separate into standalone open source package?


class Kind(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"


class Attribute(Enum):
    SLOW = "slow"
    FLAKY = "flaky"


# Test stages to run in order
TEST_STAGES = (Kind.UNIT, Kind.INTEGRATION, Kind.E2E)


def pytest_runtest_setup() -> None:
    """Disable socket for whole tests by default. But unix sockets are allowed for async support."""
    disable_socket(allow_unix_socket=True)


def pytest_collection_modifyitems(config: Config, items: list[Function]) -> None:
    """Apply rules for marks. Details are in `pyproject.toml` file."""
    for item in items:
        keywords = item.keywords

        # Correct some misuses
        if set(keywords) & {"db", "transactional_db"}:
            raise RuntimeError('use `django_db` mark instead of "db" or "transactional_db"')

        # Determine test kind
        kinds = {e.value for e in Kind}
        match len(ins := set(keywords) & kinds):
            # Defaults to unit test
            case 0:
                item.add_marker(pytest.mark.unit)
                kind = Kind.UNIT

            case 1:
                kind = Kind(ins.pop())

            case _:
                raise RuntimeError("only one of marker in {} can be used", ", ".join(map(repr, kinds)))

        # Apply rules by test kind
        match kind:
            case Kind.UNIT:
                # Unit tests not allowed use real db transactions
                m: Mark | None = keywords.get("django_db")
                if (m is not None) and (m.kwargs.get("transaction") is True):
                    raise RuntimeError(f"unit tests not allowed to use transactional databases: {item.name}")

            case Kind.INTEGRATION:
                # Enable networking in localhost only
                item.add_marker(pytest.mark.allow_hosts(["127.0.0.1"]))

                # Enable database transactions
                if "django_db" not in keywords:
                    item.add_marker(pytest.mark.django_db(transaction=True))

            case Kind.E2E:
                # Allow sockets
                item.add_marker(pytest.mark.enable_socket)

        # Find attributes from keywords
        attributes = {Attribute(attribute) for attribute in set(keywords) & {e.value for e in Attribute}}

        # Apply rules for attributes
        if Attribute.SLOW in attributes:
            if "slow" not in keywords:
                item.add_marker(pytest.mark.timeout(300))

        if Attribute.FLAKY in attributes:
            if "xfail" not in keywords:
                item.add_marker(pytest.mark.xfail(reason="This test is known as flaky, allowing it to failure."))


# Things globally used
# ============================================================================
@pytest.fixture(autouse=True)
def media_storage(settings: LazySettings, tmpdir: py.path.local) -> None:
    """Replace media storage with temporary directory while testing."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(scope="session")
def datadir() -> Path:
    """Path for data directory used for testing."""
    return Path(__file__).parent / "_data"


@pytest.fixture
def datafile(datadir: Path, request: SubRequest) -> Any:  # pylint: disable=redefined-outer-name
    """Read `datadir / request.param` (indirect parametrization) content as JSON.

    NOTE: https://docs.pytest.org/en/latest/example/parametrize.html#apply-indirect-on-particular-arguments
    TODO: Consider adding support of various file extensions (.yaml, .toml, ...)
    """
    with (datadir / str(request.param)).open(mode="r", encoding="utf-8") as f:
        json_obj = json.load(f)

    return json_obj


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Temporary fix for RuntimeError while running all tests.

    https://stackoverflow.com/questions/61022713/pytest-asyncio-has-a-closed-event-loop-but-only-when-running-all-tests
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop

    loop.close()
