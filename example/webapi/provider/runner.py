from lf2.api.data import Request
from lf2.task.router import Router
from lf2.task.runner import Runner


def resolve(router: Router, request: Request) -> Runner:
    return router.resolve(request.method, request.path)
