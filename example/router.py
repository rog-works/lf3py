from framework.api.data import Request
from framework.api.router import Router
from framework.lang.module import load_module
from framework.task.runner import Runner

routes = {
    'GET /users': ('example.controllers.users', 'index'),
    r'GET /users/\d+': ('example.controllers.users', 'show'),
    'POST /users': ('example.controllers.users', 'create'),
}


def resolve(request: Request) -> Runner:
    path, module = Router(routes).resolve(request.method, request.path)
    return load_module(path, module)
