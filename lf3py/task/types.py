from typing import Callable, Dict, Type

from lf3py.lang.dsn import DSN
from lf3py.task.result import Result

Runner = Callable[..., Result]
RunnerDecorator = Callable[[Runner], Runner]
DSNType = Type[DSN]


class Routes(Dict[str, str]): pass
