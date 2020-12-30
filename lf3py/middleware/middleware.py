from typing import Dict, Tuple

from lf3py.di.function import invoke, currying
from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.sequence import first
from lf3py.lang.locator import ILocator
from lf3py.middleware.types import ErrorMiddleware, PerformMiddleware
from lf3py.task.types import Runner, RunnerDecorator


class Middleware:
    def __init__(self) -> None:
        self._performers: Dict[Runner, Tuple[PerformMiddleware]] = {}
        self._error_handlers: Dict[Runner, Tuple[ErrorMiddleware]] = {}

    def attach(self, *performers: PerformMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.performer_register(runner, *performers)
            return runner

        return decorator

    def error(self, *error_handlers: ErrorMiddleware) -> RunnerDecorator:
        def decorator(runner: Runner) -> Runner:
            self.error_handler_register(runner, *error_handlers)
            return runner

        return decorator

    def performer_register(self, runner: Runner, *performers: PerformMiddleware):
        self._performers[runner] = performers

    def error_handler_register(self, runner: Runner, *error_handlers: ErrorMiddleware):
        self._error_handlers[runner] = error_handlers

    def build_performer(self, runner: Runner, locator: ILocator) -> 'Performer':
        return Performer(locator, self._performers.get(runner, ()), self._error_handlers.get(runner, ()))


class Performer:
    def __init__(self, locator: ILocator, performers: Tuple[PerformMiddleware, ...], error_handlers: Tuple[ErrorMiddleware, ...]) -> None:
        self._locator = locator
        self._performers = performers
        self._error_handlers = error_handlers

    def perform(self):
        for performer in self._performers:
            invoke(self._locator, performer)

    def handle_error(self, error: Exception):
        self.__handle_error(error, *self._error_handlers)

    def __handle_error(self, error: Exception, *error_handlers: ErrorMiddleware):
        for index, error_handler in enumerate(error_handlers):
            func_anno = FunctionAnnotation(error_handler)
            arg_anno = first(func_anno.args.values())
            error_types = [arg_anno.origin] if not arg_anno.is_union else [anno.origin for anno in arg_anno.union_values]
            handlable = [error_type for error_type in error_types if isinstance(error, error_type)]
            if not handlable:
                continue

            try:
                curried = currying(self._locator, error_handler)
                curried(error)
            except Exception as e:
                self.__handle_error(e, *error_handlers[index + 1:])
                raise
