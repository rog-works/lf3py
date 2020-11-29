import re
from typing import Any, Dict


class Router:
    def __init__(self, routes: Dict[str, Any]) -> None:
        self._routes = routes

    def resolve(self, *routes) -> Any:
        route = ' '.join(routes)
        for pattern, target in self._routes.items():
            if re.search(f'^{pattern}$', route):
                return target

        raise AssertionError()
