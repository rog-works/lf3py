import re
from typing import Callable, Dict

from framework.task.runner import Runner


class Router:
    def __init__(self, routes: Dict[str, Callable]) -> None:
        self._routes = routes

    def resolve(self, *routes) -> Runner:
        for pattern, factory in self._routes.items():
            route = ' '.join(routes)
            if re.search(f'^{pattern}$', route):
                return factory()

        raise ModuleNotFoundError()
