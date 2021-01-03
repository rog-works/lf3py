from types import TracebackType
from typing import Dict, List, Optional, Type

from lf3py.di.invoker import invoke, currying
from lf3py.lang.module import import_module
from lf3py.middleware.types import CatchMiddleware, AttachMiddleware
from lf3py.session import Session
from lf3py.task import Task
from lf3py.task.types import Runner, RunnerDecorator


class Middleware:
    def __init__(self) -> None:
        self._attaches: Dict[Runner, List[AttachMiddleware]] = {}
        self._catches: Dict[Runner, List[CatchMiddleware]] = {}

    def attach(self, *attaches: AttachMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.attach_register(runner, *attaches)
            return runner

        return decorator

    def catch(self, *catches: CatchMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.catch_register(runner, *catches)
            return runner

        return decorator

    def attach_register(self, runner: Runner, *attaches: AttachMiddleware):
        if runner not in self._attaches:
            self._attaches[runner] = []

        self._attaches[runner].extend(list(attaches))

    def catch_register(self, runner: Runner, *catches: CatchMiddleware):
        if runner not in self._catches:
            self._catches[runner] = []

        self._catches[runner].extend(list(catches))

    def perform(self, session: Session, task: Task) -> 'Performer':
        middleware = self.__dirty_resolve_middleware(task.runner)
        return Performer(
            session,
            middleware._attaches.get(task.runner, []),
            middleware._catches.get(task.runner, [])
        )

    def __dirty_resolve_middleware(self, runner: Runner) -> 'Middleware':
        modules = import_module(runner.__module__)
        for module in modules.__dict__.values():
            if hasattr(module, 'locate') and callable(module.locate) and hasattr(module.locate, '__self__'):
                return module.locate(Middleware)

        return self


class Performer:
    def __init__(self, session: Session, attaches: List[AttachMiddleware], catches: List[CatchMiddleware]) -> None:
        self._session = session
        self._attaches = reversed(attaches)
        self._catches = reversed(catches)

    def __enter__(self):
        self.perform()

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[BaseException], exc_traceback: TracebackType):
        if exc_value is not None:
            self.handle_error(exc_value)

    def perform(self):
        for attach in self._attaches:
            invoke(self._session, attach)

    def handle_error(self, error: BaseException):
        self.__handle_error(error, *self._catches)

    def __handle_error(self, error: BaseException, *catches: CatchMiddleware):
        for index, catch in enumerate(catches):
            try:
                curried = currying(self._session, catch)
                curried(error)
            except Exception as e:
                self.__handle_error(e, *catches[index + 1:])
                raise
