import re

from lf3py.config import ModuleDefinitions
from lf3py.di import DI
from lf3py.lang.module import load_module_path


def locator(modules: ModuleDefinitions) -> DI:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        if re.search(r'^[\w\d]+\.[\w\d]+', symbol_module_path):
            symbol = load_module_path(symbol_module_path)
            di.register(symbol, load_module_path(inject_module_path))
        else:
            module = load_module_path(inject_module_path)
            di.register(module, module)

    return di
