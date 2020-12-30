from typing import Any, Callable, Dict, Type, TypeVar

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.inspect import default_args
from lf3py.lang.locator import ILocator

_T = TypeVar('_T')


def invoke(locator: ILocator, func: Callable[..., _T]) -> _T:
    func_anno, defaults = FunctionAnnotation(func), default_args(func)
    inject_kwargs = {
        key: __resolve_arg(locator, key, arg_anno.org_type, defaults)
        for key, arg_anno in func_anno.args.items()
    }
    return func(**inject_kwargs)


def currying(locator: ILocator, func: Callable[..., _T]) -> Callable[..., _T]:
    func_anno, defaults = FunctionAnnotation(func), default_args(func)
    inject_kwargs = {
        key: __resolve_arg(locator, key, arg_anno.org_type, defaults)
        for key, arg_anno in func_anno.args.items()
        if locator.can_resolve(arg_anno.org_type) or key in defaults
    }

    def curried_func(*args, **kwargs) -> _T:
        return func(*args, **{**inject_kwargs, **kwargs})

    return curried_func


def __resolve_arg(locator: ILocator, key: str, symbol: Type, defaults: Dict[str, Any]) -> bool:
    if __allow_default(locator, key, symbol, defaults):
        return defaults[key]
    else:
        return locator.resolve(symbol)


def __allow_default(locator: ILocator, key: str, symbol: Type, defaults: Dict[str, Any]) -> bool:
    return not locator.can_resolve(symbol) and key in defaults
