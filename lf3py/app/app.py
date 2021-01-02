from typing import Type, TypeVar

from lf3py.app.provider import di_container
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.lang.locator import Locator, T_INST
from lf3py.lang.sequence import last
from lf3py.middleware.middleware import ErrorMiddleware, Middleware, PerformMiddleware
from lf3py.session.session import Session
from lf3py.task import Task, TaskQueue
from lf3py.task.data import Result
from lf3py.task.types import RunnerDecorator

T_APP = TypeVar('T_APP', bound='App')


class App:
    @classmethod
    def entry(cls: Type[T_APP], event: dict) -> T_APP:
        di = di_container(cls.module_definitions())
        di.register(LambdaEvent, lambda: event)
        app = cls(di)
        return app

    @classmethod
    def blueprint(cls: Type[T_APP]) -> T_APP:
        di = di_container(cls.module_definitions())
        return cls(di)

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self, locator: Locator) -> None:
        self._locator = locator

    def locate(self, symbol: Type[T_INST]) -> T_INST:
        return self._locator.resolve(symbol)

    def behavior(self, *perform_middlewares: PerformMiddleware) -> RunnerDecorator:
        return self.locate(Middleware).effect(*perform_middlewares)

    def on_error(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        return self.locate(Middleware).catch(*error_handlers)

    def run(self) -> Result:
        with self.__start() as session:
            results = [self.__run_task(session, task) for task in session(TaskQueue)]
            return last(results)

    def __start(self) -> Session:
        return Session.start(self._locator)

    def __run_task(self, session: Session, task: Task) -> Result:
        with session(Middleware).attach(session, task):
            return task.run()
