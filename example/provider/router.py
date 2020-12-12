from lf2.api.path import PathDSN
from lf2.task.router import Router, Routes


def make_router(routes: Routes) -> Router:
    return Router(PathDSN, routes)
