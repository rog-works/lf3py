from lf3py.config import ModuleDefinitions
from lf3py.di import DI
from lf3py.lang.module import load_module_path


def locator(modules: ModuleDefinitions) -> DI:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        symbol = load_module_path(symbol_module_path)
        injector = load_module_path(inject_module_path)
        di.register(symbol, injector)

    return di
