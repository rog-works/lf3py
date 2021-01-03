from typing import Any, Callable

Func = Callable[..., Any]
Decorator = Callable[[Func], Func]


class Embed:
    def produce(self, media_type: str) -> Decorator:
        def decorator(func: Func) -> Func:
            func.__openapi__ = {'produce': [media_type]}
            return func

        return decorator

    def consume(self, media_type: str) -> Decorator:
        def decorator(func: Func) -> Func:
            func.__openapi__ = {'consume': [media_type]}
            return func

        return decorator

    def security(self, security: dict) -> Decorator:
        def decorator(func: Func) -> Func:
            func.__openapi__ = {'security': [security]}
            return func

        return decorator

    def responses(self, status: int, response: dict) -> Decorator:
        def decorator(func: Func) -> Func:
            func.__openapi__ = {'responses': {status: response}}
            return func

        return decorator


embed = Embed()
