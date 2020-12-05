from framework.api.data import Request
from framework.api.router import resolver
from framework.lang.module import load_module
from framework.task.runner import Runner

from example.config.routes import Routes


def resolve(routes: Routes, request: Request) -> Runner:
    return load_module(*resolver(routes, request.method, request.path))
