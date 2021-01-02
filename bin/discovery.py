from pprint import pprint
import sys
from typing import List, Optional, Tuple

from lf3py.lang.module import import_module
from lf3py.lang.sequence import flatten


def discovery(*filepaths: str) -> dict:
    paths = [to_path(filepath) for filepath in filepaths]
    routes = flatten([to_routes_tuple(path) for path in paths])
    return dict(routes)


def to_path(filepath: str) -> str:
    return '.'.join('.'.join(filepath.split('.')[:-1]).split('/'))


def to_routes_tuple(path: str) -> List[Tuple[str, str]]:
    routes = dirty_resolve_routes(path)
    if not routes:
        return []

    return [(dsn_spec, module_path) for dsn_spec, module_path in routes.items()]


def dirty_resolve_routes(path: str) -> Optional[dict]:
    modules = import_module(path)
    for module in modules.__dict__.values():
        if hasattr(module, 'route') and callable(module.route) and hasattr(module.route, '_routes'):
            return module.route._routes

    return None


if __name__ == '__main__':
    _, *filepaths = sys.argv
    pprint(discovery(*filepaths), indent=4)
