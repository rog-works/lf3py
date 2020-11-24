from typing import Callable, Dict

from framework.task.runner import Runner


class Router:
    def __init__(self, routes: Dict[str, Callable]) -> None:
        self._routes = routes

    def resolve(self, *routes) -> Runner:
        for path, factory in self._routes.items():
            if ' '.join(routes) == path:
                return factory()

        raise ModuleNotFoundError()
