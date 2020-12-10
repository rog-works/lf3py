from typing import Type, TypeVar, Union


from framework.app import App
from framework.lang.di import DI
from framework.lang.module import load_module_path

_T = TypeVar('_T', bound=App)


def app_provider(app_type: Type[_T], modules: Union[dict, list]) -> _T:
    di = DI()
    if type(modules) is dict:
        for symbol_module_path, inject_module_path in modules.items():
            symbol = load_module_path(symbol_module_path)
            di.register(symbol, load_module_path(inject_module_path))
    else:
        for module_path in modules:
            module = load_module_path(module_path)
            di.register(module, load_module_path(module_path))

    return app_type(di)
