from lf3py.lang.locator import Locator
from typing import List, Tuple

from lf3py.di.invoker import currying
from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.sequence import first
from lf3py.routing.invoker import resolve_args
from lf3py.routing.symbols import IDispatcher, IRouter
from lf3py.routing.types import CatchMiddleware, Middleware
from lf3py.task.task import Catch, Task
from lf3py.task.data import Command


class Dispatcher(IDispatcher):
    def __init__(self, router: IRouter, command: Command) -> None:
        spec, attaches, catches = self.__dispatch(router, command)
        self._spec = spec
        self._command = command
        self._attaches = attaches
        self._catches = catches

    def __dispatch(self, router: IRouter, command: Command) -> Tuple[str, List[Middleware], List[CatchMiddleware]]:
        spec, middlewares = router.resolve(command.dsn.to_str())
        attaches = []
        catches = []
        for middleware in middlewares:
            func_anno = FunctionAnnotation(middleware)
            args = func_anno.args
            if args and issubclass(first(args.values()).origin, Exception):
                catches.append(middleware)
            else:
                attaches.append(middleware)

        return spec, attaches, catches

    def tasks(self, locator: Locator) -> List[Task]:
        def make_task(middleware: Middleware) -> Task:
            inject_kwargs = resolve_args(middleware, self._command, self._spec)
            curried = currying(locator, middleware)
            return Task(lambda: curried(**inject_kwargs))

        return [make_task(middleware) for middleware in self._attaches]

    def catches(self, locator: Locator) -> List[Catch]:
        def make_catch(middleware: CatchMiddleware) -> Catch:
            inject_kwargs = resolve_args(middleware, self._command, self._spec)
            curried = currying(locator, middleware)
            return Catch(lambda error: curried(error, **inject_kwargs))

        return [make_catch(middleware) for middleware in self._catches]
