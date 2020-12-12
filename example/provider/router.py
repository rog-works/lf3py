from framework.api.path import PathDSN
from framework.task.router import Router, Routes


def make_router(routes: Routes) -> Router:
    return Router(PathDSN, routes)
