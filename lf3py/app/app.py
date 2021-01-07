from typing import List, Type, TypeVar

from lf3py.app.provider import di_container
from lf3py.app.types import Blueprint
from lf3py.aws.types import LambdaEvent
from lf3py.config import ModuleDefinitions
from lf3py.lang.locator import T_INST
from lf3py.lang.sequence import last
from lf3py.routing.symbols import IRouter
from lf3py.routing.types import AttachMiddleware, CatchMiddleware, RunnerDecorator
from lf3py.session.session import Session
from lf3py.task.data import Command, CommandQueue, Result
from lf3py.task.task import Catch

T_APP = TypeVar('T_APP', bound='App')


class App:
    @classmethod
    def entry(cls: Type[T_APP], event: dict) -> T_APP:
        app = cls()
        app.__di.register(LambdaEvent, lambda: event)
        return app

    @classmethod
    def blueprint(cls) -> Blueprint:
        return cls()

    @classmethod
    def module_definitions(cls) -> ModuleDefinitions:
        raise NotImplementedError()

    def __init__(self) -> None:
        self.__di = di_container(self.module_definitions())

    def locate(self, symbol: Type[T_INST]) -> T_INST:
        return self.__di.resolve(symbol)

    def behavior(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        return self.locate(IRouter).overlap(*attaches)

    def on_error(self, *catches: CatchMiddleware) -> RunnerDecorator:
        return self.locate(IRouter).overlap(*catches)

    @property
    def route(self) -> IRouter:
        return self.locate(IRouter)

    def run(self) -> Result:
        with Session.start(self.__di) as session:
            results = [self.__run_task(session, command) for command in session(CommandQueue)]
            return last(results)

    def __run_task(self, session: Session, command: Command) -> Result:
        dispatcher = session(IRouter).dispatch(command)
        try:
            results = [task() for task in dispatcher.tasks(session)]
            return last([result for result in results if result is not None])
        except Exception as e:
            self.__handle_error(e, dispatcher.catches(session))
            raise

    def __handle_error(self, error: Exception, catches: List[Catch]):
        for index, catch in enumerate(catches):
            try:
                catch(error)
            except Exception as e:
                self.__handle_error(e, catches[index + 1:])
                raise
