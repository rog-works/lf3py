from typing import Any, Tuple, Union

from lf3py.lang.annotation import FunctionAnnotation
from lf3py.routing.errors import UnresolvedArgumentsError
from lf3py.serialization.errors import DeserializeError
from lf3py.task.data import Command, Result
from lf3py.task.types import Runner


def invoke(runner: Runner, command: Command, dsn_spec: str) -> Result:
    kwargs = resolve_args(runner, command, dsn_spec)
    return runner(**kwargs)


def resolve_args(runner: Runner, command: Command, dsn_spec: str) -> Union[Tuple[Any, dict], dict]:
    try:
        func_anno = FunctionAnnotation(runner)

        dsn_params = command.dsn.capture(dsn_spec)
        dsn_kwargs = {
            key: int(dsn_params[key]) if arg_anno.origin is int else dsn_params[key]
            for key, arg_anno in func_anno.args.items()
            if key in dsn_params
        }

        body_kwargs = {
            key: command.data(arg_anno.origin)
            for key, arg_anno in func_anno.args.items()
            if key not in dsn_kwargs
        }

        inject_kwargs = {**dsn_kwargs, **body_kwargs}
        if func_anno.is_method:
            return func_anno.receiver, inject_kwargs
        else:
            return inject_kwargs
    except (DeserializeError, KeyError, ValueError) as e:
        raise UnresolvedArgumentsError() from e
