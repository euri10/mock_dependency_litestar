from unittest import mock

import pytest
from litestar.testing import TestClient

from mock_dependency_litestar.main import create_app


def new_dependency():
    return "bar"


@pytest.fixture(autouse=True)
def mock_db():
    return mock.patch("dependencies.some_dependency", new=new_dependency)


@pytest.fixture
def app():
  return create_app()


def test(app):
    with TestClient(app) as client:
        assert client.get("/").text == "bar"