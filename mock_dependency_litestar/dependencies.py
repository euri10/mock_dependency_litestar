from typing import AsyncGenerator

from httpx import AsyncClient
from litestar.datastructures import State


def some_dependency() -> str:
    return "foo"


def get_httpx_client(state: State) -> AsyncGenerator[AsyncClient, None]:
    _client = state.httpx_client
    yield _client
