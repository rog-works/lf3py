from importlib import import_module
import sys
from typing import Any


def load_module(path: str, module: str) -> Any:
    return getattr(import_module(path), module)


def unload_module(path: str):
    if path not in sys.modules:
        raise ModuleNotFoundError()

    del sys.modules[path]
