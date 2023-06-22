from litestar import Litestar, get
from litestar.di import Provide



@get()
def handler(dep: str) -> str:
  return dep


def create_app() -> Litestar:
  from mock_dependency_litestar.dependencies import some_dependency
  return Litestar([handler], dependencies={"dep": Provide(some_dependency)})