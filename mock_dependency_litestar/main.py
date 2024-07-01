from contextlib import asynccontextmanager
from typing import AsyncGenerator

from httpx import AsyncClient
from litestar import Litestar, get, Response
from litestar.di import Provide


@get("/dep1")
def handler_dep1(dep1: str) -> str:
    return dep1


@get("/dep_httpx")
async def handler_dep_httpx(httpx_client: AsyncClient) -> str:
    response = await httpx_client.get("http://example.com/")
    return Response(response.text, status_code=response.status_code)


@asynccontextmanager
async def lifespan(
        _app: Litestar,
) -> AsyncGenerator[None, None]:
    _client = AsyncClient()
    _app.state.httpx_client = _client
    try:
        yield
    finally:
        await _client.aclose()


def create_app() -> Litestar:
    from mock_dependency_litestar.dependencies import some_dependency
    from mock_dependency_litestar.dependencies import get_httpx_client
    return Litestar([handler_dep1,
                     handler_dep_httpx
                     ],
                    dependencies={"dep1": Provide(some_dependency),
                                  "httpx_client": Provide(get_httpx_client)
                                  },
                    lifespan=[lifespan])
