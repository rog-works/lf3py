from importlib import import_module
from typing import Any


def load_module(path: str, module: str, **kwargs) -> Any:
    return getattr(import_module(path), module)(**kwargs)
