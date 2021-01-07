from typing import Any, Tuple, Union

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.routing.errors import UnresolvedArgumentsError
from lf3py.routing.types import Middleware
from lf3py.serialization.deserializer import Deserializer
from lf3py.serialization.errors import DeserializeError
from lf3py.task.data import Command


def resolve_args(middleware: Middleware, command: Command, dsn_spec: str) -> Union[Tuple[Any, dict], dict]:
    try:
        func_anno = FunctionAnnotation(middleware)

        dsn_params = command.dsn.capture(dsn_spec)
        dsn_kwargs = {
            key: int(dsn_params[key]) if arg_anno.origin is int else dsn_params[key]
            for key, arg_anno in func_anno.args.items()
            if key in dsn_params
        }

        body_kwargs = {
            key: command.data(arg_anno.origin)
            for key, arg_anno in func_anno.args.items()
            if key not in dsn_kwargs and not arg_anno.is_generics and issubclass(arg_anno.origin, Deserializer)
        }

        inject_kwargs = {**dsn_kwargs, **body_kwargs}
        if func_anno.is_method:
            return func_anno.receiver, inject_kwargs
        else:
            return inject_kwargs
    except (DeserializeError, KeyError, ValueError) as e:
        raise UnresolvedArgumentsError(e) from e
