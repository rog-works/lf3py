from importlib import import_module
from typing import Any


def load_module(path: str, module: str) -> Any:
    return getattr(import_module(path), module)
