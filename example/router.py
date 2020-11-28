from framework.api.data import Request
from framework.api.router import Router
from framework.lang.module import load_module
from framework.task.runner import Runner


def resolve(request: Request) -> Runner:
    routes = {
        'GET /users': lambda: load_module('example.controllers.users', 'index'),
        r'GET /users/\d+': lambda: load_module('example.controllers.users', 'show'),
        'POST /users': lambda: load_module('example.controllers.users', 'create'),
    }
    return Router(routes).resolve(request.method, request.path)
