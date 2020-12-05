import re
from typing import Dict, TypeVar

_T = TypeVar('_T')


def resolver(routes: Dict[str, _T], *route_elems: str) -> _T:
    route = ' '.join(route_elems)
    for pattern, target in routes.items():
        if re.search(f'^{pattern}$', route):
            return target

    raise LookupError(f'Missing route. route = {route}')
