from typing import Any, Callable

from lf3py.aws.types import LambdaHandler


def hook(method: Callable) -> Callable[[Any, LambdaHandler], LambdaHandler]:
    def wrapper(self, handler: LambdaHandler) -> LambdaHandler:
        def wrap_handler(event: dict, context: object) -> Any:
            method(self, event, context)
            return handler(event, context)

        return wrap_handler

    return wrapper
