from lf3py.config import ModuleDefinitions
from lf3py.di import DI
from lf3py.lang.locator import Locator
from lf3py.lang.module import load_module_path


def locator(modules: ModuleDefinitions) -> Locator:
    di = DI()
    for symbol_module_path, inject_module_path in modules.items():
        di.register(
            load_module_path(symbol_module_path),
            load_module_path(inject_module_path)
        )

    return di
