from typing import Any, Tuple, Union

from lf3py.api.errors import BadRequestError
from lf3py.lang.annotation import FunctionAnnotation
from lf3py.lang.error import raises
from lf3py.serialization.deserializer import DictDeserializer
from lf3py.serialization.errors import DeserializeError
from lf3py.task.types import Runner


@raises(BadRequestError, DeserializeError, KeyError, ValueError)
def resolve_args(runner: Runner, path_params: dict, params: dict) -> Union[Tuple[Any, dict], dict]:
    func_anno = FunctionAnnotation(runner)

    path_kwargs = {
        key: int(path_params[key]) if arg_anno.origin is int else path_params[key]
        for key, arg_anno in func_anno.args.items()
        if key in path_params
    }

    deserializer = DictDeserializer()
    body_kwargs = {
        key: deserializer.deserialize(arg_anno.origin, params)
        for key, arg_anno in func_anno.args.items()
        if key not in path_kwargs
    }

    inject_kwargs = {**path_kwargs, **body_kwargs}
    if func_anno.is_method:
        return func_anno.receiver, inject_kwargs
    else:
        return inject_kwargs
