from typing import Type, TypeVar

from lf3py.app.provider import di_container
from lf3py.app.types import IBlueprinter
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.lang.locator import T_INST
from lf3py.lang.sequence import last
from lf3py.middleware import Middleware
from lf3py.middleware.types import AttachMiddleware, CatchMiddleware
from lf3py.routing.symbols import IRouter
from lf3py.session.session import Session
from lf3py.task import Task, TaskQueue
from lf3py.task.data import Result
from lf3py.task.types import RunnerDecorator

T_APP = TypeVar('T_APP', bound='App')


class App:
    @classmethod
    def entry(cls: Type[T_APP], event: dict) -> T_APP:
        app = cls()
        app.__di.register(LambdaEvent, lambda: event)
        return app

    @classmethod
    def blueprint(cls) -> IBlueprinter:
        return cls()

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self) -> None:
        self.__di = di_container(self.module_definitions())

    def locate(self, symbol: Type[T_INST]) -> T_INST:
        return self.__di.resolve(symbol)

    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self.locate(Middleware).attach(*attaches)

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        return self.locate(Middleware).catch(*catches)

    @property
    def route(self) -> IRouter:
        return self.locate(IRouter)

    def run(self) -> Result:
        with self.__start() as session:
            results = [self.__run_task(session, task) for task in session(TaskQueue)]
            return last(results)

    def __start(self) -> Session:
        return Session.start(self.__di)

    def __run_task(self, session: Session, task: Task) -> Result:
        with session(Middleware).perform(session, task):
            return task.run()
