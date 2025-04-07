from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Required for pytest-asyncio to run async tests using the asyncio backend.
    """
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    """
    FastAPI sync client used for base_url.
    """
    yield TestClient(app)


@pytest_asyncio.fixture()
async def async_client(client: TestClient) -> AsyncGenerator:
    """
    Async test client that uses FastAPI’s ASGI app via httpx's ASGITransport.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac
