import traceback
from typing import Any, Callable, List, Type

from framework.errors import Error


def stacktrace(error: Exception) -> List[str]:
    return traceback.format_exception(type(error), error, error.__traceback__)


def raises(raise_error: Type[Error], *handle_errors: Type[Exception]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(wrapper_func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return wrapper_func(*args, **kwargs)
            except handle_errors as e:
                raise raise_error() from e

        return wrapper

    return decorator
