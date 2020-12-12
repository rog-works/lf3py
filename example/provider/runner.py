from framework.api.data import Request
from framework.task.router import Router
from framework.task.runner import Runner


def resolve(router: Router, request: Request) -> Runner:
    return router.resolve(request.method, request.path)
