from unittest import mock

import pytest
from httpx import AsyncClient, MockTransport, Response

from litestar.testing import TestClient, AsyncTestClient
from lxml.html import fromstring

from mock_dependency_litestar.main import create_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


def new_dependency():
    return "bar"


@pytest.fixture
def mock_db():
    with mock.patch("mock_dependency_litestar.dependencies.some_dependency", new=new_dependency):
        yield


async def new_client():
    yield AsyncClient(transport=MockTransport(
        lambda request: Response(419
                                 , content="FOO NOT FOUND"
                                 )
    ))


@pytest.fixture
def mock_httpx_client():
    with mock.patch("mock_dependency_litestar.dependencies.get_httpx_client", new=new_client):
        yield


@pytest.fixture
def mocked_app(mock_db, mock_httpx_client):
    return create_app()


@pytest.fixture
def normal_app():
    return create_app()


def test_dep1(normal_app):
    with TestClient(normal_app) as client:
        assert client.get("/dep1").text == "foo"


def test_dep1_mocked(mocked_app):
    with TestClient(mocked_app) as client:
        assert client.get("/dep1").text == "bar"


@pytest.mark.anyio
async def test_dep_httpx(normal_app):
    async with AsyncTestClient(normal_app) as client:
        response = await client.get("/dep_httpx")
        assert response.status_code == 200
        html = fromstring(response.text)
        assert html.xpath("//title/text()")[0] == "Example Domain"


@pytest.mark.anyio
async def test_dep_httpx_mocked(mocked_app):
    async with AsyncTestClient(mocked_app) as client:
        response = await client.get("/dep_httpx")
        assert response.status_code == 419
        assert response.text == "FOO NOT FOUND"
