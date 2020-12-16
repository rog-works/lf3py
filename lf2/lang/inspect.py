import inspect
from typing import Any, Callable, Dict


def default_args(func: Callable) -> Dict[str, Any]:
    sig = inspect.signature(func)
    return {
        key: param.default
        for key, param in sig.parameters.items()
        if param.default is not getattr(inspect, '_empty')
    }
