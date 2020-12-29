from lf3py.task.types import RunnerDecorator
from lf3py.lang.dsn import DSNElement
from lf3py.routing.routers.types import IRouter
from lf3py.session import Session
from lf3py.task.data import Command, Result


class RootRouter(IRouter):
    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    def __router(self) -> IRouter:
        return self._session.current().locator.resolve(IRouter)

    def __call__(self, *spec_elems: DSNElement) -> RunnerDecorator:
        return self.__router(*spec_elems)

    def dispatch(self, command: Command) -> Result:
        return self.__router.dispatch(command)
