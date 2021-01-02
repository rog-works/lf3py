from types import TracebackType
from typing import Dict, List, Optional, Type

from lf3py.di.invoker import invoke, currying
from lf3py.lang.module import import_module
from lf3py.middleware.types import ErrorMiddleware, PerformMiddleware
from lf3py.session import Session
from lf3py.task import Task
from lf3py.task.types import Runner, RunnerDecorator


class Middleware:
    def __init__(self) -> None:
        self._performers: Dict[Runner, List[PerformMiddleware]] = {}
        self._error_handlers: Dict[Runner, List[ErrorMiddleware]] = {}

    def effect(self, *performers: PerformMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.performer_register(runner, *performers)
            return runner

        return decorator

    def catch(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.error_handler_register(runner, *error_handlers)
            return runner

        return decorator

    def performer_register(self, runner: Runner, *performers: PerformMiddleware):
        self._performers[runner] = list(performers)

    def error_handler_register(self, runner: Runner, *error_handlers: ErrorMiddleware):
        self._error_handlers[runner] = list(error_handlers)

    def attach(self, session: Session, task: Task) -> 'Performer':
        middleware = self.__dirty_resolve_middleware(task.runner)
        return Performer(
            session,
            middleware._performers.get(task.runner, []),
            middleware._error_handlers.get(task.runner, [])
        )

    def __dirty_resolve_middleware(self, runner: Runner) -> 'Middleware':
        modules = import_module(runner.__module__)
        for module in modules.__dict__.values():
            if hasattr(module, 'locate') and callable(module.locate) and hasattr(module.locate, '__self__'):
                return module.locate(Middleware)

        return self


class Performer:
    def __init__(self, session: Session, performers: List[PerformMiddleware], error_handlers: List[ErrorMiddleware]) -> None:
        self._session = session
        self._performers = performers
        self._error_handlers = error_handlers

    def __enter__(self):
        self.perform()

    def __exit__(self, exc_type: Type[Exception], exc_value: Optional[BaseException], exc_traceback: TracebackType):
        if exc_value is not None:
            self.handle_error(exc_value)

    def perform(self):
        for performer in self._performers:
            invoke(self._session, performer)

    def handle_error(self, error: BaseException):
        self.__handle_error(error, *self._error_handlers)

    def __handle_error(self, error: BaseException, *error_handlers: ErrorMiddleware):
        for index, error_handler in enumerate(error_handlers):
            try:
                curried = currying(self._session, error_handler)
                curried(error)
            except Exception as e:
                self.__handle_error(e, *error_handlers[index + 1:])
                raise
