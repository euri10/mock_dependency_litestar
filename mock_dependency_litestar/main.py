from litestar import Litestar, get
from litestar.di import Provide

from mock_dependency_litestar.dependencies import some_dependency


@get()
def handler(dep: str) -> str:
  return dep

def create_app() -> Litestar:
  return Litestar([handler], dependencies={"dep": Provide(some_dependency)})