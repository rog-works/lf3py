from typing import Any, Callable

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.di import DI
from lf3py.lang.sequence import first
from lf3py.middleware.types import ErrorMiddlewares, Middleware


def attach(di: DI, *middlewares: Middleware, error: ErrorMiddlewares) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            for middleware in middlewares:
                register = di.perform(middleware)
                if type(register) is tuple:
                    di.register(*register)

            try:
                return func(*args, **kwargs)
            except Exception as e:
                for error_handler in error:
                    func_anno = FunctionAnnotation(error_handler)
                    arg_anno = first(list(func_anno.args.values()))
                    error_types = [arg_anno.origin] if not arg_anno.is_union else [anno.origin for anno in arg_anno.union_values]
                    if type(e) in error_types:
                        error_handler(e)

                raise

        return wrapper

    return decorator
