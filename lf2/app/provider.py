import re
from typing import Dict, Type, TypeVar

from lf2.app.app import App
from lf2.lang.di import DI
from lf2.lang.module import load_module_path

_T = TypeVar('_T', bound=App)


def app_provider(app_type: Type[_T], modules: Dict[str, str]) -> _T:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        if re.search(r'^[\w\d]+\.[\w\d]+', symbol_module_path):
            symbol = load_module_path(symbol_module_path)
            di.register(symbol, load_module_path(inject_module_path))
        else:
            module = load_module_path(inject_module_path)
            di.register(module, module)

    return app_type(di)
