from typing import Any, Callable

from lf3py.di.function import invoke, currying
from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.sequence import first
from lf3py.locator.types import ILocator
from lf3py.middleware.types import ErrorMiddlewares, Middleware


def attach(locator: ILocator, *middlewares: Middleware, error: ErrorMiddlewares) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                __perform_middleware(locator, *middlewares)
                return func(*args, **kwargs)
            except Exception as e:
                __handle_error(locator, e, error)
                raise

        return wrapper

    return decorator


def __perform_middleware(locator: ILocator, *middlewares: Middleware):
    for middleware in middlewares:
        invoke(locator, middleware)


def __handle_error(locator: ILocator, error: Exception, error_handlers: ErrorMiddlewares):
    for index, error_handler in enumerate(error_handlers):
        func_anno = FunctionAnnotation(error_handler)
        arg_anno = first(func_anno.args.values())
        error_types = [arg_anno.origin] if not arg_anno.is_union else [anno.origin for anno in arg_anno.union_values]
        handlable = [error_type for error_type in error_types if isinstance(error, error_type)]
        if not handlable:
            continue

        try:
            curried = currying(locator, error_handler)
            curried(error)
        except Exception as e:
            __handle_error(locator, e, error_handlers[index + 1:])
            raise
