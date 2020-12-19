import re
from typing import Optional, Type, TypeVar

from lf3py.app.app import App
from lf3py.config import ModuleDefinitions
from lf3py.lang.di import DI
from lf3py.lang.module import load_module_path

_T = TypeVar('_T', bound=App)


def app_provider(app_type: Type[_T], module_definitions: Optional[ModuleDefinitions] = None) -> _T:
    di = DI()
    modules = module_definitions if module_definitions is not None else app_type.module_definitions()
    for symbol_module_path, inject_module_path in modules.items():
        if re.search(r'^[\w\d]+\.[\w\d]+', symbol_module_path):
            symbol = load_module_path(symbol_module_path)
            di.register(symbol, load_module_path(inject_module_path))
        else:
            module = load_module_path(inject_module_path)
            di.register(module, module)

    return app_type(di)
