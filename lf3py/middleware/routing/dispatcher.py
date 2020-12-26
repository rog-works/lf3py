from lf3py.routing.routers import Router
from lf3py.task.data import Command, Result


def dispatch(command: Command, router: Router) -> Result:
    return router.dispatch(command)
