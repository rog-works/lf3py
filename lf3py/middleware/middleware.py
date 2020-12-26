from typing import Any, Callable

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.di import DI
from lf3py.lang.sequence import first
from lf3py.middleware.types import ErrorMiddlewares, Middleware


def attach(di: DI, *middlewares: Middleware, error: ErrorMiddlewares) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                __perform_middleware(di, *middlewares)
                return func(*args, **kwargs)
            except Exception as e:
                __handle_error(e, error)
                raise

        return wrapper

    return decorator


def __perform_middleware(di: DI, *middlewares: Middleware):
    for middleware in middlewares:
        register = di.perform(middleware)
        if type(register) is tuple:
            di.register(*register)


def __handle_error(error: Exception, error_handlers: ErrorMiddlewares):
    for index, error_handler in enumerate(error_handlers):
        func_anno = FunctionAnnotation(error_handler)
        arg_anno = first(list(func_anno.args.values()))
        error_types = [arg_anno.origin] if not arg_anno.is_union else [anno.origin for anno in arg_anno.union_values]
        handled = [error_type for error_type in error_types if isinstance(error, error_type)]
        if not handled:
            continue

        try:
            error_handler(error)
        except Exception as e:
            __handle_error(e, error_handlers[index + 1:])
            raise
